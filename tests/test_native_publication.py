"""Exercise CMake's symbol separation with a real ELF shared library."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


@unittest.skipUnless(
    all(shutil.which(tool) for tool in ("cc", "cmake", "objcopy", "strip", "readelf")),
    "ELF build tools are required",
)
class NativePublicationTests(unittest.TestCase):
    def test_publication_preserves_runtime_exports_and_separates_debug_info(self):
        script = Path(__file__).resolve().parents[1] / "native/publish_libraries.cmake"
        with tempfile.TemporaryDirectory(prefix="android symbols ") as temporary:
            root = Path(temporary)
            source = root / "player.c"
            source.write_text("int exported_answer(void) { return 42; }\n", encoding="utf-8")
            library = root / "libplayer.so"
            subprocess.run(["cc", "-shared", "-fPIC", "-g", str(source), "-o", str(library)], check=True)
            original = library.read_bytes()
            subprocess.run([
                "cmake", f"-DPLAYER_FILES={library}", f"-DPLAYER_DIR={root / 'package'}",
                f"-DSYMBOLS_DIR={root / 'symbols'}", f"-DOBJCOPY={shutil.which('objcopy')}",
                f"-DSTRIP={shutil.which('strip')}", "-P", str(script),
            ], check=True)
            runtime = root / "package/jniLibs/libplayer.so"
            self.assertEqual(library.read_bytes(), original)
            self.assertTrue((root / "symbols/libplayer.so.debug").is_file())
            self.assertLess(runtime.stat().st_size, len(original))
            sections = subprocess.check_output(["readelf", "-S", str(runtime)], text=True)
            self.assertNotIn(".debug_info", sections)
            self.assertIn(".gnu_debuglink", sections)
            exports = subprocess.check_output(["readelf", "--dyn-syms", str(runtime)], text=True)
            self.assertIn("exported_answer", exports)
