export const formatDate = (isoString: string) => {
  try {
    return new Date(isoString).toLocaleString();
  } catch {
    return isoString;
  }
};
