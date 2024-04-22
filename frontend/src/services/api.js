// hit localhost when developing locally
export const API_ENDPOINT = import.meta.env.PROD
  ? "/api"
  : "http://localhost:3000";

export const getWord = async () => {
  const response = await fetch(`${API_ENDPOINT}/words`);
  return await response.json();
};
