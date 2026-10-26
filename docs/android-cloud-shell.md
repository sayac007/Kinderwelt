# Upload key using Azure Cloud Shell

Use this operator-run alternative when the Windows computer cannot install a
JDK. Azure Cloud Shell runs Bash or PowerShell in the browser; local Windows
administrator rights are not needed. This guide uses **PowerShell in Azure Cloud
Shell**, not the Windows PowerShell installation. It is documentation only:
no real upload key was created or placed in a repository/CI artifact by Codex.

Microsoft documents Java among Cloud Shell's preinstalled tools. Check the
actual session before starting; do not assume a particular JDK version. The
operator needs their own authorized Azure access. Company Azure access/allowed
execution is controlled by the organization; this procedure does not bypass it.

## 1. Open the browser terminal

Open [Azure Cloud Shell](https://shell.azure.com/), sign in and choose
**PowerShell**. An ephemeral session without mounted storage is sufficient if
available in the account. Persistent Azure Files storage is not needed for this
one-time operation; do not create a storage resource just for this guide.

```powershell
Get-Command keytool -ErrorAction Stop
keytool -help
```

If `keytool` is unavailable, stop and report that message. Do not generate a
substitute key with an unreviewed web converter. No private value is needed to
report tool availability.

**Back up before closing the session.** Cloud Shell sessions time out after
20 minutes without interactive activity. Ephemeral files disappear with the
session. With persistent storage, the home directory can be saved in Azure
Files; this guide puts working files outside the home directory instead.

## 2. Create the operator's upload key interactively

Run these commands in that Cloud Shell PowerShell session. Passwords are entered
only at Java's hidden prompts, never as command-line arguments or YAML values.
Choose a strong password and save it in the operator's password manager. When
asked for the private-key password, pressing Enter uses the keystore password;
then both password Secrets below have the same value. The certificate identity
questions are completed by the operator.

```powershell
$kwKeyDir = Join-Path ([System.IO.Path]::GetTempPath()) ("kinderwelt-upload-" + [Guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $kwKeyDir -ErrorAction Stop | Out-Null
& chmod 700 $kwKeyDir
if ($LASTEXITCODE -ne 0) { throw "Cannot restrict key directory access" }
$kwKeyPath = Join-Path $kwKeyDir "kinderwelt-upload.jks"
& keytool -genkeypair -storetype JKS -keystore $kwKeyPath -alias upload -keyalg RSA -keysize 3072 -validity 10000
if ($LASTEXITCODE -ne 0) { throw "Key creation failed; do not continue" }
& chmod 600 $kwKeyPath
if ($LASTEXITCODE -ne 0) { throw "Cannot restrict key file access" }
```

The new random directory avoids overwriting an existing key. Generate this key
once and reuse it for future uploads; this command is not part of every Android
build. The alias is **`upload`**, matching the command. The key is an upload key,
not an app-signing key obtained from Google, and not the development APK key.

## 3. Prepare the GitHub value without printing it

```powershell
$kwSecretPath = Join-Path $kwKeyDir "KINDERWELT_UPLOAD_KEYSTORE.txt"
$kwEncoded = [Convert]::ToBase64String([System.IO.File]::ReadAllBytes($kwKeyPath))
[System.IO.File]::WriteAllText($kwSecretPath, "base64:" + $kwEncoded, [System.Text.UTF8Encoding]::new($false))
Remove-Variable kwEncoded
& chmod 600 $kwSecretPath
if ($LASTEXITCODE -ne 0) { throw "Cannot restrict encoded key file access" }
Write-Host "Download the keystore: $kwKeyPath"
Write-Host "Download the encoded Secret: $kwSecretPath"
```

This writes one line with the required `base64:` prefix, no BOM, whitespace or
newline. It prints **paths only**. Base64 is encoding, not encryption; the text
file contains the same sensitive keystore material. Do not print its contents,
commit either file, attach them to a PR, or send them in chat.

Use Cloud Shell's file-management **Download** action with each full path shown
above. Downloading files does not require installing a JDK on Windows. Securely
back up the `.jks` file and password(s), including an encrypted offline copy,
before ending the session. If downloading is prohibited by the device's policy,
use an authorized storage/backup method rather than bypassing that policy.

## 4. Set the four environment Secrets

First protect GitHub environment **`release`** with the `main`-only deployment
rule and a required human reviewer, as described in
[the release handoff](play/PUBLICATION.md#signing-configuration).

| Environment Secret | Operator-supplied value |
|---|---|
| `KINDERWELT_UPLOAD_KEYSTORE` | Entire single-line contents of the downloaded `.txt`, including `base64:` |
| `KINDERWELT_UPLOAD_ALIAS` | `upload`, from the actual key-generation command |
| `KINDERWELT_UPLOAD_STORE_PASSWORD` | Password entered at the keystore prompt |
| `KINDERWELT_UPLOAD_KEY_PASSWORD` | Private-key password; same as store password if Enter was chosen |

Use GitHub's **Environment secrets** UI, not repository variables or source
files. Open/copy the downloaded text through an authorized private editor; do not
use a public online Base64 service. After the four values and a usable backup are
confirmed, remove the temporary Cloud Shell working directory:

```powershell
Remove-Item -LiteralPath $kwKeyDir -Recurse -Force -ErrorAction Stop
```

The downloaded encoded text can also be removed after the Secret is saved and
the keystore/password backup is verified. Retain the actual operator key and
passwords safely. Only then run **Neutral upload-signed AAB (manual)** on `main`;
[the handoff](play/PUBLICATION.md) describes the actual signing/export checks.
A newly created key alone is not a signed or verified AAB.

## What about YAML?

Azure DevOps YAML can automate this on a manually started isolated agent, but it
requires an Azure DevOps project, suitable service permissions, and a protected
durable destination such as the operator's Key Vault. Key/password output must
not enter logs, ordinary artifacts, repository files or automatic per-build
regeneration. Copying a YAML file alone does not establish secure custody or
configure GitHub's environment Secrets. Interactive Cloud Shell is the shorter
path for this one-time setup. No Azure resource or new key-generation workflow
is deployed by this documentation change.

## Sources and verification scope

[Cloud Shell overview](https://learn.microsoft.com/en-us/azure/cloud-shell/overview),
[features and tools](https://learn.microsoft.com/en-us/azure/cloud-shell/features),
[storage persistence](https://learn.microsoft.com/en-us/azure/cloud-shell/persisting-shell-storage).
Their official [MicrosoftDocs sources](https://github.com/MicrosoftDocs/azure-docs/tree/main/articles/cloud-shell)
were read through GitHub on 2026-10-26: Java, PowerShell, ephemeral sessions,
persistent home storage and the interactive idle timeout are documented there.
A live operator Cloud Shell session and these key-generation commands have not
been executed by Codex. No Azure access or signing credentials were supplied.
