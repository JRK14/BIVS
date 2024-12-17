export class Poll {
  constructor(id, question, options) {
    this.id = id;
    this.question = question;
    this.options = options;
    this.votes = new Map();
    this.voters = new Set();
  }

  vote(voterId, optionIndex) {
    if (this.hasVoted(voterId)) {
      throw new Error('Voter has already cast their vote');
    }
    
    if (optionIndex < 0 || optionIndex >= this.options.length) {
      throw new Error('Invalid option selected');
    }

    this.votes.set(voterId, optionIndex);
    this.voters.add(voterId);
  }

  hasVoted(voterId) {
    return this.voters.has(voterId);
  }

  getResults() {
    const results = new Array(this.options.length).fill(0);
    for (const optionIndex of this.votes.values()) {
      results[optionIndex]++;
    }
    return results;
  }

  getTotalVotes() {
    return this.voters.size;
  }
}