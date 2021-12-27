// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase {
     uint256 public tokenCounter;
     bytes32 public keyhash;
     uint256 public fee;

     constructor(address _vrfCoordinator, address _linkToken, bytes32 _keyhash, uint256 _fee) public {
         VRFConsumerBase(_vrfCoordinator, address _linkToken)
         ERC721('Doggie', 'DOG') {
             tokenCounter = 0;
             keyhash = _keyhash;
             fee = _fee;
         }
     }

}