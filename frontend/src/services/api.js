// hit localhost when developing locally
export const API_ENDPOINT = import.meta.env.PROD
  ? "/api"
  : "http://localhost:3000";

export const getWord = async () => {
  const response = await fetch(`${API_ENDPOINT}/words`);
  return await response.json();
};

export const search = async (words, easy) => {
  const response = await fetch(`${API_ENDPOINT}/search`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ terms: words, exact: !easy }),
  });
  return response.json();
};
