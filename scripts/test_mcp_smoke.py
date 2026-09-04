"""Regression coverage using the installed MCP SDK's actual result models."""

import json
import unittest

from mcp import types

from mcp_smoke import PLUGIN_ROOT, validate_headless


class HeadlessSmokeModelTests(unittest.TestCase):
    def setUp(self):
        self.expected = json.loads((PLUGIN_ROOT / "parity.json").read_text())["distribution"]
        self.initialized = types.InitializeResult(
            protocolVersion=types.LATEST_PROTOCOL_VERSION,
            capabilities=types.ServerCapabilities(),
            serverInfo=types.Implementation(name="crosstabs-headless", version="1.2.0"),
        )
        self.tools = types.ListToolsResult(tools=[
            types.Tool(name=name, inputSchema={
                "type": "object",
                "required": ["projectId", "expectedRevision", "idempotencyKey",
                             "tableIds", "definition", "approval"],
            }) for name in self.expected["headlessTools"]
        ])
        self.templates = types.ListResourceTemplatesResult(resourceTemplates=[
            types.ResourceTemplate(name="artifact", uriTemplate=uri)
            for uri in self.expected["headlessResourceTemplates"]
        ])

    def validate(self):
        return validate_headless(self.initialized, self.tools, self.templates, self.expected)

    def test_accepts_real_sdk_result_models(self):
        result = self.validate()
        self.assertEqual(result["headlessToolCount"], 29)
        self.assertEqual(result["headlessServerVersion"], "1.2.0")
        self.assertEqual(result["headlessResourceTemplates"], self.expected["headlessResourceTemplates"])

    def test_rejects_incomplete_design_schema(self):
        design = next(tool for tool in self.tools.tools if tool.name == "define_survey_design")
        design.inputSchema = {"type": "object"}
        with self.assertRaisesRegex(SystemExit, "input schema is incomplete"):
            self.validate()

    def test_rejects_wrong_resource_template(self):
        self.templates.resourceTemplates[0].uriTemplate = "crosstabs://incorrect/{id}"
        with self.assertRaisesRegex(SystemExit, "resource-template mismatch"):
            self.validate()

    def test_rejects_wrong_server_version(self):
        self.initialized.serverInfo.version = "0.0.0"
        with self.assertRaisesRegex(SystemExit, "expected headless version"):
            self.validate()


if __name__ == "__main__":
    unittest.main()
