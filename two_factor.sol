pragma solidity ^0.4.19;

// import erc 721 contract and ownable
import "./openzeppelin-solidity/contracts/ownership/Ownable.sol";
import "./openzeppelin-solidity/contracts/token/ERC721/ERC721.sol";
// TODO need to import safemath? not sure yet

contract SecondFactor is Ownable {
    //@title a contract to generate and store a key used for 2 factor authentication
    //should this be a string? YES
    string twoFactor;

    // 2 factor function private or public? and only owner
    // TODO need to change owner.sol to be private? or maybe internal 
    function _time(uint time) internal returns(uint[] time){
        // this returns unix time with the last 2 digits as 0s ex. 1539204500
        time = time - time % 100;
    }
    
    function authenticate (string hand_shake, string _owner) public view onlyOwner {
        uint time = _time(now);
        //need to figure out how to combine the time and the owner so i can hash them with the time keccak or sha256
        //you cant concatinate like python string+uint or string+string doesnt work 
        sha256(x)
    }

}