pragma solidity ^0.4.19;
// erc 721 contract import here
import "./home/john/xmen/two-factor/openzeppelin-solidity/contracts/ownership/Ownable.sol";
import "./home/john/xmen/two-factor/openzeppelin-solidity/contracts/token/ERC721/ERC721.sol";

contract SecondFactor is ownable {
    //should this be a string?
    string twoFactor;

    // 2 factor function private or public? and only owner 
    function twofactor (type name) public view onlyOWner {
        
    }

}