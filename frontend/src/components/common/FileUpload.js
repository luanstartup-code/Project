import React, { useRef, useState } from 'react';
import { useTheme } from '../../contexts/ThemeContext';
import { Upload, X, File, Image, Video, Music } from 'lucide-react';
import { cn } from '../../utils/cn';

const FileUpload = ({
  onFileSelect,
  onFileRemove,
  acceptedTypes = ['*/*'],
  maxFiles = 10,
  maxSize = 50 * 1024 * 1024, // 50MB
  placeholder = "Arraste arquivos aqui ou clique para selecionar",
  className = ""
}) => {
  const { theme, isDark } = useTheme();
  const fileInputRef = useRef(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState([]);

  const handleFileSelect = (files) => {
    const fileArray = Array.from(files);
    const validFiles = fileArray.filter(file => {
      // Verificar tipo
      if (acceptedTypes[0] !== '*/*') {
        const isValidType = acceptedTypes.some(type => {
          if (type.endsWith('/*')) {
            return file.type.startsWith(type.replace('/*', ''));
          }
          return file.type === type;
        });
        if (!isValidType) {
          alert(`Tipo de arquivo não suportado: ${file.name}`);
          return false;
        }
      }

      // Verificar tamanho
      if (file.size > maxSize) {
        alert(`Arquivo muito grande: ${file.name} (${formatFileSize(file.size)})`);
        return false;
      }

      return true;
    });

    if (selectedFiles.length + validFiles.length > maxFiles) {
      alert(`Máximo de ${maxFiles} arquivos permitido`);
      return;
    }

    const newFiles = [...selectedFiles, ...validFiles];
    setSelectedFiles(newFiles);
    onFileSelect(newFiles);
  };

  const handleFileRemove = (fileToRemove) => {
    const newFiles = selectedFiles.filter(file => file !== fileToRemove);
    setSelectedFiles(newFiles);
    onFileSelect(newFiles);
    if (onFileRemove) {
      onFileRemove(fileToRemove);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    const files = e.dataTransfer.files;
    handleFileSelect(files);
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getFileIcon = (file) => {
    if (file.type.startsWith('image/')) {
      return <Image className="w-4 h-4" />;
    } else if (file.type.startsWith('video/')) {
      return <Video className="w-4 h-4" />;
    } else if (file.type.startsWith('audio/')) {
      return <Music className="w-4 h-4" />;
    } else {
      return <File className="w-4 h-4" />;
    }
  };

  return (
    <div className={cn("space-y-4", className)}>
      {/* Upload Area */}
      <div
        className={cn(
          "border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors duration-200",
          isDragOver 
            ? "border-blue-500 bg-blue-50" 
            : isDark 
              ? "border-gray-600 hover:border-gray-500" 
              : "border-gray-300 hover:border-gray-400"
        )}
        style={{
          borderColor: isDragOver ? '#3b82f6' : theme.border.primary,
          backgroundColor: isDragOver ? (isDark ? '#1e3a8a' : '#eff6ff') : 'transparent',
        }}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={handleClick}
      >
        <Upload className={cn(
          "mx-auto h-12 w-12 mb-4",
          isDragOver 
            ? "text-blue-500" 
            : isDark ? "text-gray-400" : "text-gray-300"
        )} />
        
        <p className={cn(
          "text-sm font-medium",
          isDragOver 
            ? "text-blue-600" 
            : isDark ? "text-gray-300" : "text-gray-600"
        )}
        style={{
          color: isDragOver ? '#2563eb' : theme.text.secondary,
        }}
        >
          {placeholder}
        </p>
        
        <p className="text-xs mt-2"
          style={{
            color: theme.text.tertiary,
          }}
        >
          Máximo {maxFiles} arquivos, {formatFileSize(maxSize)} cada
        </p>

        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept={acceptedTypes.join(',')}
          onChange={(e) => handleFileSelect(e.target.files)}
          className="hidden"
        />
      </div>

      {/* Selected Files */}
      {selectedFiles.length > 0 && (
        <div className="space-y-2">
          <h4 className="text-sm font-medium"
            style={{
              color: theme.text.primary,
            }}
          >
            Arquivos Selecionados ({selectedFiles.length})
          </h4>
          
          <div className="space-y-2">
            {selectedFiles.map((file, index) => (
              <div
                key={index}
                className={cn(
                  "flex items-center justify-between p-3 rounded-lg border",
                  isDark ? "bg-gray-700 border-gray-600" : "bg-gray-50 border-gray-200"
                )}
                style={{
                  backgroundColor: theme.surface.secondary,
                  borderColor: theme.border.primary,
                }}
              >
                <div className="flex items-center space-x-3">
                  {getFileIcon(file)}
                  <div>
                    <p className="text-sm font-medium"
                      style={{
                        color: theme.text.primary,
                      }}
                    >
                      {file.name}
                    </p>
                    <p className="text-xs"
                      style={{
                        color: theme.text.tertiary,
                      }}
                    >
                      {formatFileSize(file.size)}
                    </p>
                  </div>
                </div>
                
                <button
                  onClick={() => handleFileRemove(file)}
                  className={cn(
                    "p-1 rounded-full hover:bg-red-100 transition-colors duration-200",
                    isDark ? "hover:bg-red-900" : "hover:bg-red-100"
                  )}
                >
                  <X className="w-4 h-4 text-red-500" />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default FileUpload;