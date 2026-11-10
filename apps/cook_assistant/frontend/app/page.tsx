"use client";

import ChatInput from "@/component/ChatInput";
import { useState, useEffect } from "react";

const API_BASE = "http://localhost:8000";

export default function Page() {
    const [processing, setProcessing] = useState<boolean>(false);
    const [message, setMessage] = useState<string>("");

    const handleSend = async (text: string) => {
        setProcessing(true);
        const url = new URL("/api", API_BASE);

        const res = await fetch(`${url.toString()}`, {
            method: "POST",
            body: JSON.stringify({
                query: text,
                thread_id: "1"
            }),
            headers: {
                "Content-Type": "application/json"
            }
        })
        
        const reader = res.body?.getReader();
        const decoder = new TextDecoder();

        if(!reader) {
            throw new Error("cannot read the stream data");
        }

        while (true) {
            const {done, value} = await reader.read();
            if(done) {
                break;
            }
            const msg = decoder.decode(value);
            setMessage((prev) => {
                return (prev + msg)
            })
        }

        setProcessing(false);
    }


    return (
        <div>
            <p>{message}</p>
            <ChatInput onSend={handleSend} processing={processing}></ChatInput>
        </div>
    )
}
