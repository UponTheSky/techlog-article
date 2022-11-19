// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const info = (...params: any[]): void => {
  console.log(params);
};

export const error = (error: Error): void => {
  console.error(error.message);
};
