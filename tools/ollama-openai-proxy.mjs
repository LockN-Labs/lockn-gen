#!/usr/bin/env node
import http from "node:http";

const PORT = Number(process.env.PORT || 11435);
const OLLAMA_URL = process.env.OLLAMA_URL || "http://127.0.0.1:11434";
const API_KEY = process.env.OLLAMA_API_KEY || "";

function unauthorized(res) {
  res.statusCode = 401;
  res.setHeader("Content-Type", "application/json");
  res.end(JSON.stringify({ error: { message: "unauthorized" } }));
}

function readJson(req) {
  return new Promise((resolve, reject) => {
    let body = "";
    req.on("data", (chunk) => (body += chunk));
    req.on("end", () => {
      try {
        resolve(JSON.parse(body || "{}"));
      } catch (err) {
        reject(err);
      }
    });
    req.on("error", reject);
  });
}

function writeSse(res, data) {
  res.write(`data: ${JSON.stringify(data)}\n\n`);
}

const server = http.createServer(async (req, res) => {
  if (req.method !== "POST" || req.url !== "/v1/chat/completions") {
    res.statusCode = 404;
    return res.end("Not found");
  }

  if (API_KEY) {
    const auth = req.headers["authorization"] || "";
    if (!auth.startsWith("Bearer ") || auth.slice(7) !== API_KEY) {
      return unauthorized(res);
    }
  }

  let payload;
  try {
    payload = await readJson(req);
  } catch {
    res.statusCode = 400;
    return res.end("Invalid JSON");
  }

  const stream = Boolean(payload.stream);
  const ollamaReq = http.request(
    `${OLLAMA_URL}/api/chat`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    },
    (ollamaRes) => {
      if (ollamaRes.statusCode !== 200) {
        res.statusCode = ollamaRes.statusCode || 500;
        return ollamaRes.pipe(res);
      }

      if (stream) {
        res.statusCode = 200;
        res.setHeader("Content-Type", "text/event-stream");
        res.setHeader("Cache-Control", "no-cache");
        res.setHeader("Connection", "keep-alive");

        let buffer = "";
        ollamaRes.on("data", (chunk) => {
          buffer += chunk.toString();
          let idx;
          while ((idx = buffer.indexOf("\n")) >= 0) {
            const line = buffer.slice(0, idx).trim();
            buffer = buffer.slice(idx + 1);
            if (!line) continue;
            let msg;
            try {
              msg = JSON.parse(line);
            } catch {
              continue;
            }
            if (msg?.message?.content) {
              writeSse(res, {
                id: msg.id || "ollama",
                object: "chat.completion.chunk",
                created: Math.floor(Date.now() / 1000),
                model: payload.model,
                choices: [
                  { index: 0, delta: { content: msg.message.content }, finish_reason: null },
                ],
              });
            }
            if (msg?.done) {
              writeSse(res, {
                id: msg.id || "ollama",
                object: "chat.completion.chunk",
                created: Math.floor(Date.now() / 1000),
                model: payload.model,
                choices: [
                  { index: 0, delta: {}, finish_reason: msg.done_reason || "stop" },
                ],
              });
              res.write("data: [DONE]\n\n");
              return res.end();
            }
          }
        });
        ollamaRes.on("end", () => {
          res.write("data: [DONE]\n\n");
          res.end();
        });
      } else {
        let body = "";
        ollamaRes.on("data", (chunk) => (body += chunk));
        ollamaRes.on("end", () => {
          try {
            const msg = JSON.parse(body);
            const content = msg?.message?.content ?? "";
            res.statusCode = 200;
            res.setHeader("Content-Type", "application/json");
            res.end(
              JSON.stringify({
                id: msg.id || "ollama",
                object: "chat.completion",
                created: Math.floor(Date.now() / 1000),
                model: payload.model,
                choices: [
                  { index: 0, message: { role: "assistant", content }, finish_reason: "stop" },
                ],
              })
            );
          } catch {
            res.statusCode = 500;
            res.end("Invalid response from Ollama");
          }
        });
      }
    }
  );

  ollamaReq.on("error", (err) => {
    res.statusCode = 502;
    res.end(String(err));
  });

  const forwarded = {
    model: payload.model,
    messages: payload.messages || [],
    stream: stream,
  };
  ollamaReq.write(JSON.stringify(forwarded));
  ollamaReq.end();
});

server.listen(PORT, () => {
  console.log(`ollama-openai-proxy listening on http://127.0.0.1:${PORT}`);
});
