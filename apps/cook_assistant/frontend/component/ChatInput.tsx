import { useState } from "react";

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
        <div>
            <textarea 
                value={text}
                onChange={(e) => setText(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="请描述现有的食材..."
                disabled={processing}
            />
            <button
                onClick={handleSend}
            >
                {processing?"正在处理":"发送请求"}
            </button>
        </div>
        );

}
