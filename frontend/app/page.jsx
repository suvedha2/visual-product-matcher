'use client';

import { useState } from 'react';
import { Loader2, Image as ImageIcon } from 'lucide-react';
import styles from './page.module.css';
import { UploadPanel } from '../components/UploadPanel';
import { ProductCard } from '../components/ProductCard';

export default function HomePage() {
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [preview, setPreview] = useState(null);
  const [isDragging, setIsDragging] = useState(false); // State for drag-and-drop UI

  // Reusable function to process an image file
  const processImage = async (file) => {
    if (!file) return;

    setResults([]);
    setError('');
    setIsLoading(true);
    setPreview(URL.createObjectURL(file));

    const formData = new FormData();
    formData.append('image', file);
    
    try {
      // Add this logic to use the live Render URL or default to localhost
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

const response = await fetch(`${API_URL}/api/search`, { // <-- Using the dynamic variable
  method: 'POST',
  body: formData,
});
      if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError('Failed to fetch results. Is the backend server running?');
    } finally {
      setIsLoading(false);
    }
  };

  // --- NEW: Function to handle the file input click ---
  const handleImageUpload = (event) => {
    if (event.target.files && event.target.files.length > 0) {
      processImage(event.target.files[0]);
    }
  };
  
  // --- NEW: Functions for Drag and Drop ---
  const handleDragOver = (event) => {
    event.preventDefault(); // This is crucial to allow dropping
    setIsDragging(true);
  };
  
  const handleDragLeave = (event) => {
    event.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setIsDragging(false);
    if (event.dataTransfer.files && event.dataTransfer.files.length > 0) {
      processImage(event.dataTransfer.files[0]);
      event.dataTransfer.clearData(); // Clean up
    }
  };

  // --- NEW: Function to reset the UI for a new search ---
  const resetState = () => {
    setPreview(null);
    setResults([]);
    setError('');
  };

  return (
    <main className={styles.main}>
      <div className={styles.container}>
        <header className={styles.header}>
          <h1 className={styles.title}>Visual Product Matcher</h1>
        </header>

        <UploadPanel 
          preview={preview}
          isDragging={isDragging}
          onImageUpload={handleImageUpload}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onReset={resetState}
        />

        <div>
          {isLoading && (
            <div className={styles.placeholder}>
              <Loader2 size={48} className="animate-spin" color="#4299e1" />
              <p>Finding matches...</p>
            </div>
          )}

          {!isLoading && error && <div className={styles.placeholder} style={{ color: '#e53e3e' }}>{error}</div>}

          {!isLoading && !error && results.length > 0 && (
            <div className={styles.resultsGrid}>
              {results.map((result) => (
                <ProductCard key={result.product.id} product={result.product} score={result.score} />
              ))}
            </div>
          )}

          {!isLoading && !error && results.length === 0 && (
            <div className={styles.placeholder}>
               <ImageIcon size={48} color="#a0aec0" />
               <p>Matching products will appear here.</p>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}