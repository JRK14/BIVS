import CryptoJS from 'crypto-js';

export class Voter {
  constructor(id, nationalId, publicKey) {
    this.id = id;
    this.nationalIdHash = CryptoJS.SHA256(nationalId).toString();
    this.publicKey = publicKey;
    this.votingHistory = new Set();
  }

  hasVotedInElection(electionId) {
    return this.votingHistory.has(electionId);
  }

  recordVote(electionId) {
    this.votingHistory.add(electionId);
  }

  verifyIdentity(nationalId) {
    return this.nationalIdHash === CryptoJS.SHA256(nationalId).toString();
  }
}