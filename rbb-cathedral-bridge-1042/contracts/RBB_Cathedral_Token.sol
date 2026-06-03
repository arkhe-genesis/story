// SPDX-License-Identifier: GPL-3.0
// Substrato 1042 - RBB-CATHEDRAL-BRIDGE
// Token ERC-20 Real
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

contract RBB_Cathedral_Token is ERC20, AccessControl {
    bytes32 public constant BRIDGE_ROLE = keccak256("BRIDGE_ROLE");

    constructor(address _admin) ERC20("Catedral Theosis", "THEO") {
        _grantRole(DEFAULT_ADMIN_ROLE, _admin);
    }

    function mint(address to, uint256 amount) external onlyRole(BRIDGE_ROLE) {
        _mint(to, amount);
    }

    function burn(address from, uint256 amount) external onlyRole(BRIDGE_ROLE) {
        _burn(from, amount);
    }
}
