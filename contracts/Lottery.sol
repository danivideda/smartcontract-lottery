// SPDX-License-Identifier: MIT
pragma solidity ^0.8.11;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract Lottery {
    address payable[] public players;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal priceFeed;

    constructor(address _priceFeedAddress) {
        usdEntryFee = 50 * (10**18);
        priceFeed = AggregatorV3Interface(_priceFeedAddress);
    }

    function enter() public {
        // $50 minimum to enter
        players.push(payable(msg.sender));
    }

    function getEntranceFee() public view returns (uint256) {}

    function startLottery() public {}

    function endLotter() public {}
}
