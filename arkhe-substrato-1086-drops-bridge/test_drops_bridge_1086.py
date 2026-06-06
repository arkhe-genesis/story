import pytest
from drops_bridge_1086 import DropsBridgeOrchestrator

def test_drops_bridge_orchestrator():
    orch = DropsBridgeOrchestrator()
    dashboard = orch.get_dashboard()
    assert dashboard["substrato"] == "1086"
    assert dashboard["nome"] == "DROPS-DATABASE-BRIDGE"

def test_fuse_driver():
    orch = DropsBridgeOrchestrator()
    inode = orch.fuse_driver.exec_query("SELECT 1", ())
    stats = orch.fuse_driver.get_inode_stats()
    assert stats["total_inodes"] == 1
