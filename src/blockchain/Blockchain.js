import { Block } from './Block.js';

export class Blockchain {
  constructor() {
    this.chain = [this.createGenesisBlock()];
    this.difficulty = 2;
    this.pendingVotes = [];
  }

  createGenesisBlock() {
    return new Block(Date.now(), { votes: [] }, '0');
  }

  getLatestBlock() {
    return this.chain[this.chain.length - 1];
  }

  addVote(vote) {
    this.pendingVotes.push(vote);
  }

  minePendingVotes(minerAddress) {
    const block = new Block(Date.now(), {
      votes: this.pendingVotes,
      minerAddress: minerAddress
    }, this.getLatestBlock().hash);

    block.mineBlock(this.difficulty);
    this.chain.push(block);
    this.pendingVotes = [];
  }

  isChainValid() {
    for (let i = 1; i < this.chain.length; i++) {
      const currentBlock = this.chain[i];
      const previousBlock = this.chain[i - 1];

      if (currentBlock.hash !== currentBlock.calculateHash()) {
        return false;
      }

      if (currentBlock.previousHash !== previousBlock.hash) {
        return false;
      }
    }
    return true;
  }

  getVoteResults() {
    const results = new Map();
    
    for (const block of this.chain) {
      if (block.data.votes) {
        for (const vote of block.data.votes) {
          const count = results.get(vote.candidate) || 0;
          results.set(vote.candidate, count + 1);
        }
      }
    }
    
    return results;
  }
}