"use client";

import ChatInput from "@/component/ChatInput";
import { useState, useEffect, useRef } from "react";
import { apiFetch, fetchStream } from "@/lib/api";


const path = "/api";

export interface ChatMessage {
    id: number, 
    role: "ai" | "human";
    message: string,
    thread_id: string
}

export interface ChatMessageReceived {
    role: "ai" | "human";
    message: string,
}


export default function Page() {
    // first set the messageId for sending the message, +1 for each turn
    const messageId = useRef(0);
    const [processing, setProcessing] = useState<boolean>(false);
    const [message, setMessage] = useState<string>("");
    const [thread_id, setThread_id] = useState<string | null>(null);
    const [chatMessageList, setChatMessageList] = useState<ChatMessage[]>([]);

    useEffect(() => {
        let thread_id = localStorage.getItem("thread_id");
        // Generate UUID as thread_id
        if (!thread_id) {
            thread_id = crypto.randomUUID();
            localStorage.setItem("thread_id", thread_id);
        }
        setThread_id(thread_id);
    }, [])

    const addChatMessage = (text: string, role: "ai" | "human", thread_id: string): ChatMessage => {
        const newChatMessage: ChatMessage = {
            id: messageId.current,
            role: role,
            message: text,
            thread_id: thread_id
        };
        messageId.current += 1;

        return newChatMessage;
    }

    const handleSend = async (text: string) => {
        if (!thread_id) {
            throw Error("Thread_id not set yet");
        }
        setProcessing(true);
        // clear the message before receiving the response from backend
        setMessage("");
        
        // construct the ChatMessage and messageId+1 after generating
        const newChatMessage: ChatMessage = addChatMessage(text, "human", thread_id);
        // save the user message to ChatMessage list after generating the ChatMessage
        setChatMessageList(prev => [...prev, newChatMessage]);

        try {
            // create a variable to avoid using the message state val in the snapshot
            let msg_text = "";

            await fetchStream(
                path, 
                {
                    method: "POST",
                    body: JSON.stringify({
                        query: newChatMessage.message,
                        thread_id: newChatMessage.thread_id
                    }),
                    headers: {
                        "Content-Type": "application/json"
                    }
                },
                (msg: string) => {
                    setMessage(prev => prev + msg);
                    msg_text += msg;
                }
            )
            // after receiving the complete message save the ChatMessage to list
            const aiChatMessage = addChatMessage(msg_text, "ai", thread_id);
            setChatMessageList(prev => [...prev, aiChatMessage]);

        } catch (error) {
            console.error("Chat request failed:", error);
        } finally {
            setProcessing(false);
        }
    }

    const deleteChat = async () => {
        if (!thread_id) {
            throw new Error("thread_id is not available");
        }
        try {
            await apiFetch(`/api/${thread_id}`, {
                method: "DELETE",
            });
            setMessage("");
            setChatMessageList([]);
        } catch(error) {
            console.error("Delete request failed:", error);
        }
    }

    const getChatHistory = async () => {
        if (!thread_id) {
            throw new Error("thread_id is not available");
        }
        try {
            const res = await apiFetch(`/api/${thread_id}`, {
                method: "GET",
            });
            const msgList: ChatMessageReceived[] = res;
            const chatMsgList: ChatMessage[] = msgList.map((msg, index) => {
                const msg_received: ChatMessage = {
                    id: index,
                    message: msg.message,
                    role: msg.role,
                    thread_id: thread_id
                }

                return msg_received;
            });
            setChatMessageList(chatMsgList);
            messageId.current = res.length
        } catch(error) {
            console.error("Get request failed:", error);
        }
    }

    return (
        <div className="relative h-dvh min-h-[26rem] overflow-hidden bg-gradient-to-br from-slate-50 via-white to-amber-50 text-slate-900">
            {/* The background part only for decoration*/}
            <div
                aria-hidden="true"
                className="pointer-events-none absolute -right-24 -top-24 h-80 w-80 rounded-full bg-amber-100/60 blur-3xl"
            />
            <div
                aria-hidden="true"
                className="pointer-events-none absolute -bottom-32 -left-24 h-96 w-96 rounded-full bg-slate-200/50 blur-3xl"
            />

            <div className="relative mx-auto flex h-full w-full max-w-5xl flex-col gap-4 px-4 py-4 sm:gap-5 sm:px-6 sm:py-6">
                {/* Header and two buttons at the top*/}
                <header className="flex shrink-0 flex-col gap-4 rounded-2xl border border-slate-200/80 bg-white/90 px-5 py-4 shadow-sm 
                    backdrop-blur-sm sm:flex-row sm:items-center sm:justify-between"
                >   
                    <div className="flex items-center gap-3">
                        <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-amber-600 text-lg font-semibold text-white shadow-sm">
                            厨
                        </div>
                        <div>
                            <h1 className="text-lg font-semibold tracking-tight text-slate-900 sm:text-xl">
                                AI 私人厨师
                            </h1>
                            <p className="mt-0.5 text-xs text-slate-500 sm:text-sm">
                                食材搭配与家常烹饪助手
                            </p>
                        </div>
                    </div>
                    <div className="flex flex-wrap items-center gap-2">
                        <button
                            onClick={getChatHistory}
                            disabled={processing}
                            type="button"
                            className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm font-medium text-slate-700
                            transition hover:bg-slate-50 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-amber-600"
                        >
                            查看历史(Check history chats)
                        </button>
                        <button
                            onClick={deleteChat}
                            disabled={processing}
                            type="button"
                            className="rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-sm font-medium text-amber-800 
                            transition hover:bg-amber-100 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-amber-600"
                            >
                            清空历史(Clear history chats)
                        </button>
                    </div>
                </header>
                {/* The chat window */}
                <main className="flex min-h-0 flex-1 flex-col overflow-hidden rounded-3xl border border-slate-200/80 bg-white/90 shadow-lg
                shadow-slate-200/40 backdrop-blur-sm">
                    <div className="shrink-0 border-b border-slate-100 px-5 py-4 sm:px-7">
                        <h2 className="text-sm font-semibold text-slate-700">
                            聊天窗口(ChatWindow)
                        </h2>
                    </div>

                    <section className="min-h-0 flex-1 overflow-y-auto px-5 py-6 sm:px-7">
                        {processing ? (
                            <div>
                                {chatMessageList.map((chatMessage: ChatMessage) => (
                                    <p key={chatMessage.id}
                                        className="w-fit max-w-[92%] whitespace-pre-wrap break-words rounded-2xl rounded-tl-md border border-slate-200
                                    bg-slate-50 px-5 py-4 text-sm leading-7 text-slate-700 empty:hidden sm:max-w-[85%]"
                                    >
                                        From: {chatMessage.role + " : "} {chatMessage.message}
                                    </p>
                                    ))
                                }

                                <p className="w-fit max-w-[92%] whitespace-pre-wrap break-words rounded-2xl rounded-tl-md border border-slate-200
                                    bg-slate-50 px-5 py-4 text-sm leading-7 text-slate-700 empty:hidden sm:max-w-[85%]"
                                >
                                    {message}
                                </p>
                            </div>
                        ): (
                            chatMessageList.map((chatMessage: ChatMessage) => (
                                <p key={chatMessage.id}
                                    className="w-fit max-w-[92%] whitespace-pre-wrap break-words rounded-2xl rounded-tl-md border border-slate-200
                                bg-slate-50 px-5 py-4 text-sm leading-7 text-slate-700 empty:hidden sm:max-w-[85%]"
                                >
                                    From: {chatMessage.role + " : "} {chatMessage.message}
                                </p>
                            ))
                        )}
                        
                    </section>
                    {/* Input the chat part, follows the chat window */}
                    <div className="shrink-0 border-t border-slate-200/80 bg-white px-4 py-4 sm:px-6">
                        <ChatInput onSend={handleSend} processing={processing}></ChatInput>
                    </div>
                </main>
            </div>
        </div>
    )
}
