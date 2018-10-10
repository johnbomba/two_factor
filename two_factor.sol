pragma solidity ^0.4.19;
// erc 721 contract import here
import "./openzeppelin-solidity/contracts/ownership/Ownable.sol";
import "./openzeppelin-solidity/contracts/token/ERC721/ERC721.sol";

contract SecondFactor is ownable {
    //should this be a string?
    string twoFactor;

    // 2 factor function private or public? and only owner 
    function authenticate (string hand_shake) public view onlyOwner {
        
    }

}