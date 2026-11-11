import { useState } from "react";

// 1. def the interface, onSend is the call back function and processing decides the display of the button
// and disable the button while processing
interface ChatInputProps {
  onSend: (text:string) => void
  processing?: boolean
}


export default function ChatInput({onSend, processing}: ChatInputProps) {
    const [text, setText] = useState<string>("")

    const handleSend = () => {
        if (text.trim()) {
            onSend(text.trim());
        }
        setText("");
    }

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    }

    return (
        <div className="w-full">
            <div className="flex items-end gap-3 rounded-2xl border border-slate-200 bg-slate-50/80 p-3 transition 
                focus-within:border-amber-300 focus-within:bg-white focus-within:ring-4 focus-within:ring-amber-100/60"
            >
                <label htmlFor="cook-chat-input"  className="sr-only">Please enter the info in English or Chinese:</label>
                <textarea 
                    id="cook-chat-input"
                    value={text}
                    rows={2}
                    onChange={(e) => setText(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="描述你有的食材，或问一个烹饪问题……"
                    disabled={processing}
                    className="min-h-12 min-w-0 flex-1 resize-none border-0 bg-transparent px-2 py-2 text-sm leading-6 text-slate-800 
                        outline-none placeholder:text-slate-400 disabled:cursor-not-allowed disabled:opacity-60"
                />
                <button
                    onClick={handleSend}
                    type="button"
                    disabled={processing}
                    className="inline-flex h-11 shrink-0 items-center justify-center gap-2 rounded-xl bg-amber-600 px-4 text-sm font-medium
                        text-white shadow-sm transition hover:bg-amber-700 focus-visible:outline-2 focus-visible:outline-offset-2 \
                        focus-visible:outline-amber-600 disabled:cursor-not-allowed disabled:bg-slate-300"
                >
                    {processing?"正在处理":"发送请求"}
                    
                    <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"
                        strokeLinejoin="round" className="h-4 w-4"
                    >
                        <path d="M12 19V5M5 12l7-7 7 7" />
                    </svg>
                </button>
            </div>
            <p className="mt-2 px-1 text-xs text-slate-400">Enter 发送 · Shift + Enter 换行</p>
        </div>
        );

}
