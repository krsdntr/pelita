import { env } from "cloudflare:workers";

export const prerender = false;

export async function POST({ request }) {
  const apiKey = env.GROQ_API_KEY;
  
  if (!apiKey) {
    return new Response(JSON.stringify({ error: "API Key not configured on the server." }), {
      status: 500,
      headers: { "Content-Type": "application/json" }
    });
  }

  try {
    const body = await request.json();
    
    // Validate request body
    if (!body || !body.messages) {
      return new Response(JSON.stringify({ error: "Invalid request format." }), {
        status: 400,
        headers: { "Content-Type": "application/json" }
      });
    }

    // Default to a fast model if not provided
    const model = body.model || "llama-3.1-8b-instant";

    const groqResponse = await fetch("https://api.groq.com/openai/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${apiKey}`
      },
      body: JSON.stringify({
        model: model,
        messages: body.messages
      })
    });

    const data = await groqResponse.json();

    return new Response(JSON.stringify(data), {
      status: groqResponse.status,
      headers: { "Content-Type": "application/json" }
    });

  } catch (error) {
    console.error("[Edge API Error]:", error);
    return new Response(JSON.stringify({ error: "Internal Server Error", details: error.message }), {
      status: 500,
      headers: { "Content-Type": "application/json" }
    });
  }
}
