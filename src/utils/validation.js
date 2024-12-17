export const validateNationalId = (nationalId) => {
  // This is a simplified validation - implement according to your country's ID format
  return /^\d{8,12}$/.test(nationalId);
};

export const validateElectionData = (title, candidates, startDate, endDate) => {
  if (!title || title.trim().length < 5) {
    throw new Error('Election title must be at least 5 characters long');
  }

  if (!candidates || candidates.length < 2) {
    throw new Error('Election must have at least 2 candidates');
  }

  if (!isDateValid(startDate, endDate)) {
    throw new Error('Invalid election dates');
  }
};