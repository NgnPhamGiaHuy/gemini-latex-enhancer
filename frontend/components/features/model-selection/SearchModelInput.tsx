"use client";

import { Search } from "lucide-react";

import { Input } from "@/components/ui/Input";

interface SearchModelInputProps {
    searchTerm: string;
    onSearchChange: (value: string) => void;
}

const SearchModelInput = ({
    searchTerm,
    onSearchChange,
}: SearchModelInputProps) => {
    return (
        <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
                placeholder="Search models..."
                value={searchTerm}
                onChange={(e) => onSearchChange(e.target.value)}
                className="pl-10"
            />
        </div>
    );
};

export default SearchModelInput;
