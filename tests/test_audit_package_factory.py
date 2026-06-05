from trust_engine.application.audit_package_factory import AuditPackageFactory

factory = AuditPackageFactory()
package = factory.create("TR-001", "EL-001", "DL-001")

print(package)
assert package.audit_package_id
assert package.trust_record_reference == "TR-001"
assert package.evidence_lineage_reference == "EL-001"
assert package.decision_ledger_reference == "DL-001"
assert package.created_timestamp
print("PASS")
