// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import '@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol';
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract Lottery is VRFConsumerBase, Ownable {
    address payable[] public players;
    uint256 public usdEntryFee;
    address payable public recentWinner;
    uint256 public randomnessVariable;

    AggregatorV3Interface internal ethUsdPriceFeed;
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    // 0
    // 1
    // 2
    LOTTERY_STATE public lottery_state;
    uint256 public fee;
    bytes32 public keyHash;


    constructor(
        address _priceFeedAddress, 
        address _vrfCoordinator, 
        address _link, 
        uint256 _fee,
        bytes32 _keyHash
    ) public VRFConsumerBase(_vrfCoordinator, _link){
        usdEntryFee = 50 * (10**28);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED;
        fee = _fee;
        keyHash = _keyHash;
    }
     
    function enter() public payable {
        // 50$ minimum 
        require(lottery_state == LOTTERY_STATE.OPEN);
        require(msg.value <= getEntranceFee(), "Not enough ETH");
        players.push(msg.sender);
    }

    function getEntranceFee() public view returns (uint256) {
        (,int price,,,) = ethUsdPriceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * 10**10; // 18 decimals
        uint256 costToEnter = (usdEntryFee * 10**18) / adjustedPrice;
        return costToEnter;
    }

    function startLottery() public onlyOwner {
        require(lottery_state == LOTTERY_STATE.CLOSED, "Can't start a new lottery yet!");
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public {
        // So how to create a random index value for the players array to pick a winner?
        // Hashing values doesn't make a value more random, as it gives exactly the same output for the same input every time
        // uint256(keccak256(abi.encodePacked(
        //     nonce, // nonce is predictable
        //     msg.sender, // sender address is predictable
        //     block.difficulty, // can be manipulated by miners
        //     block.timestamp // timestamp is predictable
        //     ))) % players.length;

        // Chainlink VRF offers Verifiable Randomness (provable random number)
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        bytes32 requestId = requestRandomness(keyHash, fee);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness) internal override{
        require(lottery_state == LOTTERY_STATE.CALCULATING_WINNER, "You aren't there yet!");
        require(_randomness > 0, "random-not-found");
        uint256 indexOfWinner = _randomness % players.length;
        recentWinner = players[indexOfWinner];
        recentWinner.transfer(address(this). balance);
        // Reset the lottery
        players = new address payable[](0);
        LOTTERY_STATE.CLOSED;
        randomnessVariable = _randomness;
    }
}