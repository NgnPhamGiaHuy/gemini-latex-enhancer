import React from "react";

import AlignStep from "@/components/features/AlignStep";
import UploadStep from "@/components/features/UploadStep";
import DownloadStep from "@/components/features/DownloadStep";

const Main: React.FC = () => {
    return (
        <main role="main" aria-label="Resume enhancement workflow">
            <UploadStep />
            <AlignStep />
            <DownloadStep />
        </main>
    );
};

export default Main;
