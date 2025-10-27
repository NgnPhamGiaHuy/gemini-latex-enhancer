import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface State {
    isClient: boolean;
}

const initialState: State = {
    isClient: false,
};

const clientSlice = createSlice({
    name: "client",
    initialState,
    reducers: {
        setIsClient: (state, action: PayloadAction<boolean>) => {
            state.isClient = action.payload;
        },
        toggleClient: (state) => {
            state.isClient = !state.isClient;
        },
    },
});

export const { setIsClient, toggleClient } = clientSlice.actions;
export default clientSlice.reducer;
