"use client";

import { motion } from "framer-motion";

const ModelHelpText = () => {
    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="text-xs text-foreground bg-white p-3 nb-border nb-shadow"
        >
            💡 Different models may provide varying quality and speed. Pro
            models typically offer better results but may take longer to
            process.
        </motion.div>
    );
};

export default ModelHelpText;
