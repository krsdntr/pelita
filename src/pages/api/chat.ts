import type { APIContext } from 'astro';

export const prerender = false;

export async function POST({ request, locals }: APIContext) {
  // @ts-ignore - locals.runtime.env contains Cloudflare bindings
  const env = (locals.runtime?.env as any) || import.meta.env || {};
  const apiKey = env.GROQ_API_KEY;
  
  if (!apiKey) {
    return new Response(JSON.stringify({ error: { message: "GROQ_API_KEY belum dikonfigurasi di server." } }), {
      status: 500,
      headers: { "Content-Type": "application/json" }
    });
  }

  try {
    const body = (await request.json()) as { messages?: any[]; model?: string };
    
    // Validate request body
    if (!body || !body.messages) {
      return new Response(JSON.stringify({ error: { message: "Format request tidak valid." } }), {
        status: 400,
        headers: { "Content-Type": "application/json" }
      });
    }

    // Default to Qwen model if not provided
    const model = body.model || "qwen/qwen3.8-27b";

    const groqResponse = await fetch("https://api.groq.com/openai/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${apiKey}`
      },
      body: JSON.stringify({
        model: model,
        messages: body.messages,
        max_completion_tokens: 1000
      })
    });

    const responseText = await groqResponse.text();
    let data;
    try {
      data = responseText ? JSON.parse(responseText) : {};
    } catch {
      data = { error: { message: responseText || "Respon tak dikenal dari server Groq API." } };
    }

    return new Response(JSON.stringify(data), {
      status: groqResponse.status,
      headers: { "Content-Type": "application/json" }
    });

  } catch (error: any) {
    console.error("[Edge API Error]:", error);
    return new Response(JSON.stringify({ error: { message: error.message || "Internal Server Error" } }), {
      status: 500,
      headers: { "Content-Type": "application/json" }
    });
  }
}
