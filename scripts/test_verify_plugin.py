"""Source publication is not provider-directory approval or listing."""

from copy import deepcopy
import unittest

import verify_plugin


class SourceReleaseContractTests(unittest.TestCase):
    def test_source_release_preserves_prior_evidence_and_registry_boundary(self):
        state = verify_plugin.EXPECTED_RELEASE_STATE
        self.assertEqual(state["schemaVersion"], 3)
        self.assertEqual(state["sourceRelease"]["sourceState"], "public_source_release")
        self.assertEqual(state["sourceRelease"]["tag"], "v0.3.0")
        self.assertEqual(state["sourceRelease"]["sourceReference"], "https://github.com/barangaroo/crosstabs-codex-plugin/tree/v0.3.0")
        self.assertTrue(state["sourceRelease"]["packagePublished"])
        self.assertTrue(state["sourceRelease"]["registryPublished"])
        self.assertEqual(state["previousSourceRelease"]["pluginVersion"], "0.2.6")
        self.assertEqual(state["previousSourceRelease"]["packageVersion"], "1.2.2")
        self.assertEqual(verify_plugin.EXPECTED_STATISTICS_TOOL_COUNT, 40)
        self.assertEqual(len(verify_plugin.EXPECTED_HEADLESS_TOOLS), 33)
        self.assertEqual(state["historicalPublicRelease"]["pluginVersion"], "0.2.3")
        for directory in state["directoryStatus"].values():
            self.assertEqual(directory, {"submitted": False, "approved": False, "listed": False})

    def test_rejects_directory_claims_without_receipts(self):
        for provider in ("openai", "claude"):
            for field in ("submitted", "approved", "listed"):
                with self.subTest(provider=provider, field=field):
                    state = deepcopy(verify_plugin.EXPECTED_RELEASE_STATE)
                    state["directoryStatus"][provider][field] = True
                    with self.assertRaises(ValueError):
                        verify_plugin.verify_release_state(state)

    def test_rejects_mutable_main_as_the_release_reference(self):
        state = deepcopy(verify_plugin.EXPECTED_RELEASE_STATE)
        state["sourceRelease"]["sourceReference"] = "https://github.com/barangaroo/crosstabs-codex-plugin/tree/main"
        with self.assertRaises(ValueError):
            verify_plugin.verify_release_state(state)

    def test_accepts_exact_versioned_registry_reference_separately(self):
        url = "https://registry.modelcontextprotocol.io/v0.1/servers/io.github.crosstabs%2Fcrosstabs/versions/1.3.0"
        verify_plugin.verify_registry_publication(True, url)
        verify_plugin.verify_registry_publication(False, None)

    def test_rejects_unbound_or_mutable_registry_claims(self):
        url = "https://registry.modelcontextprotocol.io/v0.1/servers/io.github.crosstabs%2Fcrosstabs/versions/1.3.0"
        for published, record in [(True, None), (False, url),
                                  (True, url.replace("1.3.0", "latest")),
                                  (True, url.replace("1.3.0", "1.2.0")),
                                  (True, url.replace("io.github.crosstabs", "io.github.other"))]:
            with self.subTest(published=published, record=record):
                with self.assertRaises(ValueError):
                    verify_plugin.verify_registry_publication(published, record)


if __name__ == "__main__":
    unittest.main()
