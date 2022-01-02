// SPDX-License-Identifier: MIT
pragma solidity ^0.8.11;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract Lottery {
    address payable[] public players;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal priceFeed;
    address owner;

    constructor(address _priceFeedAddress) {
        usdEntryFee = 50 * (10**18);
        priceFeed = AggregatorV3Interface(_priceFeedAddress);
        owner = msg.sender;
    }

    function enter() public payable {
        // $50 minimum to enter
        require(msg.value >= getEntranceFee(), "not enough ETH");
        players.push(payable(msg.sender));
    }

    function getEntranceFee() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        uint256 usdEthConversionRate = uint256(answer) *
            (10**18 / (10**priceFeed.decimals()));
        // 372600299482
        uint256 precision = 10**18;
        uint256 conversionResult = (usdEntryFee * precision) /
            usdEthConversionRate;
        // 13419205531909524 x 10^-18 = 0.013419205531909524
        // Something updated
        return uint256(conversionResult);
    }

    function startLottery() public {}

    function endLottery() public {}

    function forceWithdraw() public {
        payable(msg.sender).transfer(address(this).balance);
    }

    function getBalance() public view returns (uint256) {
        return uint256(address(this).balance);
    }
}
