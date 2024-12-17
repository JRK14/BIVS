import { v4 as uuidv4 } from 'uuid';
import { Election } from '../models/Election.js';

export class ElectionService {
  constructor(blockchain) {
    this.elections = new Map();
    this.blockchain = blockchain;
  }

  createElection(title, candidates, startDate, endDate) {
    const election = new Election(
      uuidv4(),
      title,
      candidates,
      new Date(startDate),
      new Date(endDate)
    );
    this.elections.set(election.id, election);
    return election;
  }

  getElection(id) {
    return this.elections.get(id);
  }

  getAllElections() {
    return Array.from(this.elections.values());
  }

  getActiveElections() {
    return this.getAllElections().filter(election => election.isActive());
  }

  async submitVote(electionId, voterId, candidateId) {
    const election = this.getElection(electionId);
    if (!election || !election.isActive()) {
      throw new Error('Invalid or inactive election');
    }

    const vote = {
      electionId,
      voterId,
      candidateId,
      timestamp: Date.now()
    };

    this.blockchain.addVote(vote);
    await this.blockchain.minePendingVotes(voterId);
    return true;
  }

  getElectionResults(electionId) {
    const election = this.getElection(electionId);
    if (!election) throw new Error('Election not found');

    const results = new Map();
    election.candidates.forEach(candidate => results.set(candidate.id, 0));

    const blockchainResults = this.blockchain.getVoteResults();
    blockchainResults.forEach((count, candidateId) => {
      if (results.has(candidateId)) {
        results.set(candidateId, count);
      }
    });

    return results;
  }
}