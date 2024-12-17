import { v4 as uuidv4 } from 'uuid';
import { Voter } from '../models/Voter.js';
import { ethers } from 'ethers';

export class VoterService {
  constructor() {
    this.voters = new Map();
  }

  async registerVoter(nationalId) {
    // Generate a new Ethereum-style wallet for the voter
    const wallet = ethers.Wallet.createRandom();
    
    const voter = new Voter(
      uuidv4(),
      nationalId,
      wallet.publicKey
    );
    
    this.voters.set(voter.id, voter);
    return {
      voterId: voter.id,
      publicKey: wallet.publicKey,
      privateKey: wallet.privateKey // In a real system, this would be securely delivered to the voter
    };
  }

  getVoter(id) {
    return this.voters.get(id);
  }

  verifyVoter(voterId, nationalId) {
    const voter = this.getVoter(voterId);
    if (!voter) return false;
    return voter.verifyIdentity(nationalId);
  }

  canVoteInElection(voterId, electionId) {
    const voter = this.getVoter(voterId);
    if (!voter) return false;
    return !voter.hasVotedInElection(electionId);
  }

  recordVote(voterId, electionId) {
    const voter = this.getVoter(voterId);
    if (voter) {
      voter.recordVote(electionId);
    }
  }
}