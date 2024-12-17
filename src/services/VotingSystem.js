import { v4 as uuidv4 } from 'uuid';
import { Poll } from '../models/Poll.js';

export class VotingSystem {
  constructor() {
    this.polls = new Map();
    this.voters = new Set();
  }

  createPoll(question, options) {
    const pollId = uuidv4();
    const poll = new Poll(pollId, question, options);
    this.polls.set(pollId, poll);
    return pollId;
  }

  registerVoter() {
    const voterId = uuidv4();
    this.voters.add(voterId);
    return voterId;
  }

  vote(pollId, voterId, optionIndex) {
    if (!this.voters.has(voterId)) {
      throw new Error('Invalid voter ID');
    }

    const poll = this.polls.get(pollId);
    if (!poll) {
      throw new Error('Poll not found');
    }

    poll.vote(voterId, optionIndex);
    return poll.getResults();
  }

  getPoll(pollId) {
    return this.polls.get(pollId);
  }

  getAllPolls() {
    return Array.from(this.polls.values());
  }
}