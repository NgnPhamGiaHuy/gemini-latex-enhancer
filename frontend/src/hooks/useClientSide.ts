import { useState, useEffect } from "react";

const useClientSide = (): boolean => {
    const [isClient, setIsClient] = useState(false);

    useEffect(() => {
        setIsClient(true);
    }, []);

    return isClient;
};

export default useClientSide;
