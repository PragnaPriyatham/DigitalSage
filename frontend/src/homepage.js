import React, { useState, useEffect, useRef } from 'react';
import { Search, Send } from 'lucide-react';

const AnimatedBackground = () => (
  <div className="fixed inset-0 z-0">
    <div className="absolute inset-0 bg-gradient-to-br from-gray-900 to-gray-800"></div>
    {[...Array(20)].map((_, i) => (
      <div
        key={i}
        className="absolute rounded-full bg-gray-300 opacity-10 shadow-lg"
        style={{
          top: `${Math.random() * 100}%`,
          left: `${Math.random() * 100}%`,
          width: `${Math.random() * 80 + 30}px`,
          height: `${Math.random() * 80 + 30}px`,
          animation: `float ${Math.random() * 10 + 15}s infinite ease-in-out`,
        }}
      />
    ))}
    <style>
      {`
        @keyframes float {
          0% {
            transform: translateY(0) translateX(0) scale(1);
          }
          50% {
            transform: translateY(-20px) translateX(10px) scale(1.05);
          }
          100% {
            transform: translateY(0) translateX(0) scale(1);
          }
        }
      `}
    </style>
  </div>
);

const HomePage = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [question, setQuestion] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const chatRef = useRef(null); // Reference for the chat container

  const handleQuestionSubmit = async (e) => {
    e.preventDefault();
    const data = { prompt: question };
    setChatHistory((prev) => [...prev, { role: 'user', text: question }]);
    setQuestion('');
    setLoading(true);
    setError('');

    try {
      const response = await fetch('http://localhost:8000/device/inputis', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      if (!response.ok) throw new Error('Network response was not ok');
      const result = await response.json();
      const responseText = result.error ? result.error : result.summarization;

      // Add the device's response to the chat history
      setChatHistory((prev) => [
        ...prev,
        { role: 'deviceSage', text: responseText },
      ]);
    } catch (error) {
      setError('Error sending data. Please try again.');
      console.error('Error sending data:', error);
    } finally {
      setLoading(false);
    }
  };

  // Scroll to the bottom of the chat whenever chatHistory changes
  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [chatHistory]);

  return (
    <div className="flex flex-col min-h-screen relative overflow-hidden font-sans">
      <AnimatedBackground />
      <div className="relative z-10 flex-grow flex flex-col">
        <header className="bg-white bg-opacity-10 backdrop-filter backdrop-blur-lg text-white p-4 shadow-lg">
          <div className="container mx-auto flex justify-between items-center">
            <h1 className="text-3xl font-bold">DeviceSage</h1>
            <div className="relative">
              <input
                type="text"
                placeholder="Search devices..."
                className="py-2 px-4 pr-10 rounded-full bg-white bg-opacity-20 backdrop-filter backdrop-blur-lg text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-white"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
              <Search className="absolute right-3 top-2.5 text-white" />
            </div>
          </div>
        </header>

        <main className="flex-grow container mx-auto py-12 px-4 flex flex-col max-w-5xl">
          <div
            ref={chatRef}
            className="flex flex-col space-y-4 mb-4 flex-grow scrollable max-h-[80vh] overflow-y-auto"
          >
            {chatHistory.map((chat, index) => (
              <div
                key={index}
                className={`flex ${chat.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`rounded-lg p-3 max-w-md ${
                    chat.role === 'user' ? 'bg-gray-500 text-white' : 'bg-gray-300 text-black'
                  }`}
                >
                  <p>{chat.text}</p>
                </div>
              </div>
            ))}
          </div>

          {error && <p className="text-red-500">{error}</p>}
          {loading && <p className="text-white">Loading...</p>}

          <form onSubmit={handleQuestionSubmit} className="mb-8">
            <div className="flex justify-center">
              <input
                type="text"
                placeholder="Talk to Device Sage.."
                className="w-3/4 py-3 px-2 rounded-l-lg border-t border-b border-l text-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-500"
                id="prompt"
                name="prompt"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
              />
              <button
                type="submit"
                className="border border-white to-gray-800 text-white py-3 px-6 rounded-r-lg hover:to-gray-600 transition-colors duration-300"
              >
                <Send size={20} />
              </button>
            </div>
          </form>
        </main>
      </div>

      <footer className="bg-white bg-opacity-10 backdrop-filter backdrop-blur-lg text-white py-4">
        <div className="container mx-auto text-center">
          <p>&copy; 2024 DeviceRecommender. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;
