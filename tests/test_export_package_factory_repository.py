import pytest

from trust_engine.application.export_package_factory import ExportPackageFactory
from trust_engine.infrastructure.export_package_repository import ExportPackageRepository


def test_export_package_factory_repository():
    factory = ExportPackageFactory()
    repo = ExportPackageRepository()

    package = factory.create("TR-001", "AP-001", "CLEAN_EXPORT")
    saved = repo.save(package)
    loaded = repo.get(package.export_package_id)

    assert saved == package
    assert loaded == package


def test_export_package_factory_rejects_export_embargo():
    factory = ExportPackageFactory()

    with pytest.raises(ValueError, match="EXPORT_EMBARGO is a hard stop"):
        factory.create("TR-001", "AP-001", "EXPORT_EMBARGO")