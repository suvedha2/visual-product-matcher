// components/UploadPanel.jsx
import Image from 'next/image';
import { UploadCloud } from 'lucide-react';
import styles from './UploadPanel.module.css';

export const UploadPanel = ({
  preview,
  isDragging,
  onImageUpload,
  onDragOver,
  onDragLeave,
  onDrop,
  onReset
}) => {
  return (
    <div className={styles.panel}>
      {!preview ? (
        <label
          htmlFor="file-upload"
          className={`${styles.dropzone} ${isDragging ? styles.dragging : ''}`}
          onDragOver={onDragOver}
          onDragLeave={onDragLeave}
          onDrop={onDrop}
        >
          <UploadCloud size={48} color="#a0aec0" />
          <p style={{ marginTop: '1rem', fontWeight: '500', color: '#4a5568' }}>Drop file here</p>
          <p style={{ fontSize: '0.875rem' }}>OR</p>
          <div className={styles.uploadButton}>Upload File</div>
          {/* THE FIX IS HERE: We now use our new CSS class to hide the input */}
          <input id="file-upload" type="file" className={styles.hiddenInput} accept="image/*" onChange={onImageUpload} />
        </label>
      ) : (
        <>
          <div className={styles.previewContainer}>
            <Image src={preview} alt="Uploaded preview" fill style={{ objectFit: 'cover' }} />
          </div>
          <button onClick={onReset} className={styles.uploadButton} style={{ marginTop: '1rem' }}>
            Upload Another Image
          </button>
        </>
      )}
    </div>
  );
};