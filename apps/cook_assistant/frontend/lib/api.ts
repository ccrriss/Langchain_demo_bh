export type ApiFetchOptions = RequestInit;

export const API_BASE = (() => {
    // 1. Check whether frontend, frontend: window is obj, else undefined. Checking whether window exists actually
    // if check window === undefined, will raise ReferenceError since it's not defined yet
    const isServer = typeof window === "undefined";
    if (!isServer) {
        return "";
    }
    // 2. Check whether the url comes with / at the end, if there is, remove it with re
    const serverBase = (process.env.BACKEND_URL ?? "").replace(/\/$/, "");
    return serverBase;
})();

export const apiFetch = async <T=any>(path: string, options: ApiFetchOptions): Promise<T | null> => {
    // 1. check whether path begins with /, if not add / at the beginning
    if (!path.startsWith("/")) {
        path = "/" + path;
    }
    const res = await fetch(
        `${API_BASE}${path}`,
        {
            ...options
        }
    );

    // 2. If !res.ok, throw the error
    if (!res.ok) {
        const res_body = await res.json().catch(() => ({}));
        throw new Error(`API Error ${res.status}`);
    }
    if (res.status === 204) {
        return null;
    }
    // 3. The res from backend is promised as json format, so use res.json to get the obj
    const data = await res.json() as T;
    return data;
}

export const fetchStream = async (path: string, options: RequestInit, setMsgHook: (msg: string) => void) => {
    // 1. check whether path begins with /, if not add / at the beginning
    // use hook as a reference
    if (!path.startsWith("/")) {
        path = "/" + path;
    }

    const res = await fetch(
        `${API_BASE}${path}`,
        {
            ...options
        }
    );

    // 2. get the stream output from res.body.getReader()
    const reader = res.body?.getReader();
    // 3. prepare the decoder for decoding the array from reader
    const decoder = new TextDecoder();

    if(!reader) {
        throw new Error("cannot read the stream data");
    }

    while(true) {
        // 4. use a loop to decode the streaming array and set stream to true to keep Chinese words continuous
        const {done, value} = await reader.read();
        if(done) {
            break;
        }
        const message = decoder.decode(value, {stream: true});
        setMsgHook(message)
    }
}