// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Lottery is Ownable, VRFConsumerBase {
    address payable[] public players;
    address payable public recentWinner;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    LOTTERY_STATE public lotteryState;
    event RequestedRandomness(bytes32 requestId);

    // VRF Chainlink
    bytes32 public keyHash;
    uint256 public fee;
    uint256 public randomness;

    constructor(
        address _priceFeedAddress,
        address _vrfCoordinator,
        address _link,
        bytes32 _keyHash,
        uint256 _fee
    ) public VRFConsumerBase(_vrfCoordinator, _link) {
        usdEntryFee = 50 * (10**18);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lotteryState = LOTTERY_STATE.CLOSED;

        // VRF Chainlink
        keyHash = _keyHash;
        fee = _fee;
    }

    /**
     * @dev Requests randomness
     * @return requestId unique ID for this request
     */
    function getRandomNumber() private returns (bytes32 requestId) {
        require(
            LINK.balanceOf(address(this)) >= fee,
            "Not enough LINK - fill contract with faucet"
        );
        return requestRandomness(keyHash, fee);
    }

    /**
     * @dev Withdraw all LINK token from this contract
     */
    function withdrawLink() external returns (string memory) {
        LINK.transfer(owner(), LINK.balanceOf(address(this)));
        return "Success";
    }

    function enter() external payable {
        // $50 minimum to enter
        require(lotteryState == LOTTERY_STATE.OPEN);
        require(msg.value >= getEntranceFee(), "Not enough ETH!");
        players.push(msg.sender);
    }

    function getEntranceFee() public view returns (uint256) {
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) *
            10**(18 - uint256(ethUsdPriceFeed.decimals())); // making it a 10**18 decimals
        // $50, $2000/ETH
        // 50/2000 => 50 * (10**18) / 2000
        uint256 costToEnter = (usdEntryFee * 10**18) / adjustedPrice;
        return uint256(costToEnter);
    }

    function startLottery() external onlyOwner {
        require(
            lotteryState == LOTTERY_STATE.CLOSED,
            "Can't start a Lottery a lottery yet"
        );

        lotteryState = LOTTERY_STATE.OPEN;
    }

    function endLottery() external onlyOwner {
        lotteryState = LOTTERY_STATE.CALCULATING_WINNER;
        bytes32 requestId = getRandomNumber();
        emit RequestedRandomness(requestId);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal
        override
    {
        require(
            lotteryState == LOTTERY_STATE.CALCULATING_WINNER,
            "You are not there yet"
        );
        require(_randomness > 0, "Random value not found");
        uint256 indexOfWinner = _randomness % players.length;
        recentWinner = players[indexOfWinner];

        // Give fund to winner
        recentWinner.transfer(address(this).balance);

        // Reset
        players = new address payable[](0);
        lotteryState = LOTTERY_STATE.CLOSED;
        randomness = _randomness;
    }
}
