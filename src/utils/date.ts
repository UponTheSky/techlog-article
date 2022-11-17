export const getToday = (): Date => new Date(Date.now());

export const getMonthsBefore = (months: number): Date => {
  const today = getToday();
  return new Date(today.setMonth(today.getMonth() - months));
};
