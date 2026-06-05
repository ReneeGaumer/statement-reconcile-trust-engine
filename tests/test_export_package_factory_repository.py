from trust_engine.application.export_package_factory import ExportPackageFactory
from trust_engine.infrastructure.export_package_repository import ExportPackageRepository


def test_export_package_factory_repository():
    
    factory = ExportPackageFactory()
    repo = ExportPackageRepository()
    package = factory.create("TR-001", "AP-001", "EXPORT_EMBARGO")
    
    saved = repo.save(package)
    loaded = repo.get(package.export_package_id)
    
    assert loaded == package
    assert package.trust_record_reference == "TR-001"
    assert package.audit_package_reference == "AP-001"
    assert package.export_classification == "EXPORT_EMBARGO"
    assert package.created_timestamp
    
    try:
        repo.save(package)
        raise AssertionError("Overwrite should have failed")
    except ValueError:
        print("Immutable save protection confirmed")
    
