// Verify every payload entry, without a CA trust assertion or private key.
import java.nio.file.Path;
import java.security.MessageDigest;
import java.security.cert.X509Certificate;
import java.util.HexFormat;
import java.util.jar.JarFile;

class VerifyBundle {
    public static void main(String[] args) throws Exception {
        int count = 0;
        try (var jar = new JarFile(Path.of(args[0]).toFile(), true)) {
            var entries = jar.entries();
            while (entries.hasMoreElements()) {
                var entry = entries.nextElement();
                var name = entry.getName();
                if (entry.isDirectory() || name.matches("(?i)META-INF/(MANIFEST\\.MF|[^/]+\\.(SF|RSA|DSA|EC))")) continue;
                // Reading the whole entry triggers the JDK digest/signature check.
                try (var stream = jar.getInputStream(entry)) {
                    stream.transferTo(java.io.OutputStream.nullOutputStream());
                }
                var signers = entry.getCodeSigners();
                if (signers == null || signers.length != 1) throw new SecurityException("Unsigned or multiple-signature entry");
                var cert = (X509Certificate) signers[0].getSignerCertPath().getCertificates().get(0);
                cert.checkValidity();
                var fingerprint = HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(cert.getEncoded()));
                if (!MessageDigest.isEqual(fingerprint.getBytes(java.nio.charset.StandardCharsets.US_ASCII), args[1].getBytes(java.nio.charset.StandardCharsets.US_ASCII)))
                    throw new SecurityException("Unexpected upload signer");
                count++;
            }
        }
        if (count == 0) throw new SecurityException("Empty signed archive");
        System.out.println("{\"signature\":\"VERIFIED upload certificate\",\"certificate_sha256\":\"" + args[1] + "\",\"signed_entries\":" + count + "}");
    }
}
