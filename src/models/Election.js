export class Election {
  constructor(id, title, candidates, startDate, endDate) {
    this.id = id;
    this.title = title;
    this.candidates = candidates;
    this.startDate = startDate;
    this.endDate = endDate;
    this.status = this.calculateStatus();
  }

  calculateStatus() {
    const now = new Date();
    if (now < this.startDate) return 'upcoming';
    if (now > this.endDate) return 'ended';
    return 'active';
  }

  isActive() {
    return this.calculateStatus() === 'active';
  }

  toJSON() {
    return {
      id: this.id,
      title: this.title,
      candidates: this.candidates,
      startDate: this.startDate.toISOString(),
      endDate: this.endDate.toISOString(),
      status: this.status
    };
  }
}