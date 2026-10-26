"""Release delivery must stay private, neutral, verified and a draft."""
import importlib.util,hashlib,json,os,tempfile,unittest,zipfile
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
def module(name):
    spec=importlib.util.spec_from_file_location('publication_'+name,ROOT/'scripts/android'/f'{name}.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
preflight=module('release_preflight');draft=module('draft_release')
class PublicationDeliveryTests(unittest.TestCase):
    def config(self,root):
        path=Path(root)/'scripts/android';path.mkdir(parents=True)
        (path/'release-metadata.json').write_text(json.dumps(dict(publisher='Synthetic fixture',support_email='fixture@example.invalid',asset_license='{{DECISION}}')))
    def fixture(self,root):
        root=Path(root);bundle=root/draft.BUNDLE
        with zipfile.ZipFile(bundle,'w') as archive:archive.writestr('assetPackInstallTime/assets/assets/quest/cast.json',json.dumps({'variant':'public'}))
        item={'bytes':bundle.stat().st_size,'sha256':hashlib.sha256(bundle.read_bytes()).hexdigest()}
        proof=dict(source_tracking='git-worktree',source_dirty=False,git_state_changed_during_build=False,source_commit='1'*40,variant='public',signing={'aab':'UPLOAD_SIGNED','upload_certificate_sha256':'a'*64},package=draft.identity.CONFIG['release_package'],version_name=draft.identity.CONFIG['version_name'],version_code=draft.identity.CONFIG['version_code'],artifacts={draft.BUNDLE:item})
        verified={**item,**{k:proof[k] for k in ['package','version_name','version_code']},'permissions':[],'allow_backup':False}
        (root/'provenance.json').write_text(json.dumps(proof));(root/'verification.json').write_text(json.dumps({'status':'PASS','artifacts':{draft.BUNDLE:verified}}))
        # Tempting but forbidden attachments must never enter the allowlist.
        (root/'private.keystore').write_text('NOT A KEY');(root/'aab.log').write_text('raw diagnostics')
        return proof
    def test_preflight_uses_approved_metadata_fallback_and_only_names_missing_fields(self):
        with tempfile.TemporaryDirectory() as d:
            self.config(d);env={name:'synthetic-only' for name in preflight.upload_signing.REQUIRED}
            env['KINDERWELT_PUBLISHER']='';env['KINDERWELT_SUPPORT_EMAIL']=''
            self.assertEqual(preflight.missing(env,Path(d)),['KINDERWELT_ASSET_LICENSE'])
            env['KINDERWELT_ASSET_LICENSE']='Operator fixture decision'
            self.assertEqual(preflight.missing(env,Path(d)),[])
            value=preflight.upload_signing.metadata(env,Path(d))
            self.assertEqual(value['publisher'],'Synthetic fixture');self.assertEqual(value['support_email'],'fixture@example.invalid')
    def test_confirmed_release_namespace_is_required_without_changing_test_updates(self):
        self.assertEqual(draft.identity.validate_configured_release_package('io.github.sayac007.kinderwelt'),'io.github.sayac007.kinderwelt')
        with self.assertRaisesRegex(ValueError,'operator-confirmed'):draft.identity.validate_configured_release_package('io.github.sayac007.other')
        self.assertEqual(draft.identity.CONFIG['test_package'],'org.example.kinderwelt');self.assertEqual(draft.identity.CONFIG['preview_channel'],'v090')
    def test_valid_bundle_is_cryptographically_rechecked_and_files_are_allowlisted(self):
        with tempfile.TemporaryDirectory() as d,patch.object(draft.upload_signing,'verify') as verify:
            proof=self.fixture(d);got,files=draft.validate(Path(d),Path('/tools'))
            self.assertEqual(got,proof);self.assertEqual({f.name for f in files},{draft.BUNDLE,'provenance.json','verification.json'})
            verify.assert_called_once_with(Path(d)/draft.BUNDLE,Path('/tools/android-jdk'),'a'*64)
    def test_modified_unsigned_family_dirty_and_wrong_identity_bundles_fail_before_network(self):
        for changed in ['modified','unsigned','family','dirty','package','report','version']:
            with self.subTest(changed=changed),tempfile.TemporaryDirectory() as d,patch.object(draft.upload_signing,'verify'):
                root=Path(d);proof=self.fixture(root)
                if changed=='modified':(root/draft.BUNDLE).write_bytes(b'changed')
                elif changed=='unsigned':proof['signing']['aab']='UNSIGNED'
                elif changed=='family':proof['variant']='family'
                elif changed=='dirty':proof['source_dirty']=True
                elif changed=='package':proof['package']='de.other.app'
                elif changed=='version':proof['version_code']=1
                elif changed=='report':(root/'verification.json').write_text('{"status":"FAIL"}')
                (root/'provenance.json').write_text(json.dumps(proof))
                with self.assertRaises(ValueError):draft.validate(root,Path('/tools'))
    def test_public_repository_is_rejected_without_creating_a_release(self):
        with tempfile.TemporaryDirectory() as d,patch.object(draft.upload_signing,'verify'),patch.object(draft,'gh',return_value='{"private":false}') as gh:
            self.fixture(d)
            with self.assertRaisesRegex(ValueError,'private repository'):draft.deliver(Path(d),Path('/tools'),'owner/repo','123.1')
            self.assertEqual(gh.call_count,1)
    def test_delivery_creates_a_draft_for_the_exact_source_without_a_publish_command(self):
        with tempfile.TemporaryDirectory() as d,patch.object(draft.upload_signing,'verify'),patch.object(draft,'gh',side_effect=['{"private":true}','', '{"url":"https://github.com/owner/repo/releases/test","isDraft":true}']) as gh:
            proof=self.fixture(d);result=draft.deliver(Path(d),Path('/tools'),'owner/repo','123.1')
            create=gh.call_args_list[1].args
            self.assertEqual(create[:2],('release','create'));self.assertIn('--draft',create);self.assertIn(proof['source_commit'],create)
            self.assertNotIn('--latest',create);self.assertTrue(result['isDraft'])
    def test_draft_workflow_is_manual_main_environment_guarded_and_has_no_family_token(self):
        text=(ROOT/'.github/workflows/android-release-draft.yml').read_text()
        self.assertIn('workflow_dispatch:',text);self.assertNotIn('  push:',text);self.assertNotIn('pull_request:',text)
        self.assertIn("github.ref == 'refs/heads/main'",text);self.assertIn('environment: release',text);self.assertIn('persist-credentials: false',text)
        self.assertIn('contents: write',text);self.assertIn("data.get('private') is not True",text);self.assertIn('draft_release.py',text)
        self.assertNotIn('FAMILY_ASSETS',text);self.assertNotIn('upload-artifact@',text)
