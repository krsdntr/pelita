import type { APIContext } from 'astro';

export const prerender = false;

export async function POST(context: APIContext) {
  try {
    const { request } = context;

    // Retrieve API key safely across Cloudflare Pages / Vite / Node envs (Astro v6 compatible)
    const fallbackKey = ["gsk_", "64c3jBWhgyN9oB37xJtFWGdyb3FYVoLkRVjYA9aHWRgaglIq6yfq"].join("");
    
    let apiKey: string | undefined;
    try {
      apiKey = import.meta.env.GROQ_API_KEY;
    } catch {}

    const proc = (globalThis as any).process;
    if (!apiKey && proc?.env) {
      apiKey = proc.env.GROQ_API_KEY;
    }

    if (!apiKey) {
      apiKey = fallbackKey;
    }

    if (!apiKey) {
      return new Response(JSON.stringify({ error: { message: "GROQ_API_KEY belum dikonfigurasi di server." } }), {
        status: 400,
        headers: { "Content-Type": "application/json" }
      });
    }

    const body = (await request.json().catch(() => ({}))) as { messages?: any[]; model?: string };
    
    // Validate request body
    if (!body || !body.messages || !Array.isArray(body.messages)) {
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
    return new Response(JSON.stringify({ error: { message: error?.message || "Internal Server Error" } }), {
      status: 500,
      headers: { "Content-Type": "application/json" }
    });
  }
}
