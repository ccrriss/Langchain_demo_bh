"use client";

import ChatInput from "@/component/ChatInput";
import { useState, useEffect } from "react";
import { apiFetch, fetchStream, API_BASE } from "@/lib/api";

const path = "/api";

export default function Page() {
    const [processing, setProcessing] = useState<boolean>(false);
    const [message, setMessage] = useState<string>("");

    const handleSend = async (text: string) => {
        setProcessing(true);

        try {
            await fetchStream(
                path, 
                {
                    method: "POST",
                    body: JSON.stringify({
                        query: text,
                        thread_id: "1"
                    }),
                    headers: {
                        "Content-Type": "application/json"
                    }
                },
                (msg: string) => {
                    setMessage(prev => prev + msg);
                }
            )
        } catch (error) {
            console.error("Chat request failed:", error);
        } finally {
            setProcessing(false);
        }
    }

    const deleteChat = async () => {
        const thread_id = "1";
        const url = new URL(`/api/${thread_id}`, API_BASE);
        try {
            await apiFetch(url.toString(), {
                method: "DELETE",
            })
        } catch(error) {
            console.error("Delete request failed:", error);
        }
    }

    const getChatHistory = async () => {
        const thread_id = "1";
        const url = new URL(`/api/${thread_id}`, API_BASE);
        try {
            const res = await apiFetch(url.toString(), {
                method: "GET",
            })
            setMessage((prev) => {
                return (prev + res.join())
            })
        } catch(error) {
            console.error("Get request failed:", error);
        }
    }

    return (
        <div>
            <div>
                <p>{message}</p>
            </div>
            <ChatInput onSend={handleSend} processing={processing}></ChatInput>
            <button onClick={deleteChat}>Detele current chat</button>
            <button onClick={getChatHistory}>Get chat history</button>
        </div>
    )
}
