import React from "react";

interface WrapperProps {
    children: React.ReactNode;
}

const Wrapper: React.FC<WrapperProps> = ({ children }) => {
    return (
        <div className="min-h-screen bg-gradient-to-br from-background via-background to-muted/20">
            <div className="max-w-7xl mx-auto p-2 sm:p-4 lg:p-6 container">
                {children}
            </div>
        </div>
    );
};

export default Wrapper;
