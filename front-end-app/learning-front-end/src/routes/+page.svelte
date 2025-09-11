<script lang="ts">
    import { onMount } from 'svelte';
    let question: string = '';
    let answer: string = '';
    let loading: boolean = false;
    let error: string = '';

    async function askQuestion() {
        answer = '';
        error = '';
        loading = true;
        try {
            const res = await fetch('http://127.0.0.1:5000/research', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ prompt: question })
            });
            if (!res.ok) {
                const errorText = await res.text();
                throw new Error(`Error: ${res.status}, ${errorText}`);
            }
            const data = await res.json();
            answer = data ?? 'No answer received.';
        } catch (e) {
            error = e instanceof Error ? e.message : 'Unknown error';
        } finally {
            loading = false;
        }
    }
</script>

<main class="flex flex-col items-center justify-center min-h-screen bg-gray-50">
    <div class="bg-white shadow-lg rounded-lg p-8 w-full max-w-md">
        <h1 class="text-2xl font-bold mb-6 text-gray-800 text-center">Ask a Question</h1>
        <form on:submit|preventDefault={askQuestion} class="flex flex-col gap-4">
            <input
                type="text"
                bind:value={question}
                placeholder="Type your question..."
                required
                class="border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
            />
            <button
                type="submit"
                disabled={loading}
                class="bg-blue-600 text-white font-semibold py-2 rounded hover:bg-blue-700 transition disabled:opacity-50"
            >
                Ask
            </button>
        </form>

        {#if loading}
            <p class="mt-4 text-blue-600 text-center">Loading...</p>
        {/if}

        {#if answer}
            <p class="mt-4 text-green-700 text-center"><strong>Answer:</strong> {answer}</p>
        {/if}

                {#if error}
                    <p class="mt-4 text-red-600 text-center"><strong>Error:</strong> {error}</p>
                {/if}
            </div>
        </main>