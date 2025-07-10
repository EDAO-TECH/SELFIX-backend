// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import "@openzeppelin/contracts-upgradeable/token/ERC20/extensions/ERC20BurnableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";

contract SFXCToken is Initializable, ERC20BurnableUpgradeable, OwnableUpgradeable, UUPSUpgradeable {
    function initialize(uint256 initialSupply) public initializer {
        __ERC20_init("SELFIX Core", "SFXC");
        __ERC20Burnable_init();
        __Ownable_init(msg.sender); // ✅ Fix: Explicit owner
        __UUPSUpgradeable_init();

        _mint(msg.sender, initialSupply);
    }

    function _authorizeUpgrade(address newImplementation) internal override onlyOwner {}
}
