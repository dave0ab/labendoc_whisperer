// Example: Async Transcription with Status Polling
// This shows how to handle the 504 timeout issue by using async processing

class AsyncTranscriptionClient {
  constructor(baseUrl, authToken) {
    this.baseUrl = baseUrl;
    this.authToken = authToken;
    this.headers = {
      'Authorization': `Bearer ${authToken}`,
      'Content-Type': 'application/json'
    };
  }

  // Start transcription job
  async startTranscription(audioFile, assessmentId) {
    const formData = new FormData();
    formData.append('audio', audioFile);
    formData.append('assessmentId', assessmentId);

    try {
      const response = await fetch(`${this.baseUrl}/api/v1/transcription/transcribe`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.authToken}`
        },
        body: formData
      });

      if (response.status === 202) {
        const data = await response.json();
        console.log('✅ Transcription job started:', data);
        return data.data.jobId;
      } else {
        throw new Error(`Failed to start transcription: ${response.status}`);
      }
    } catch (error) {
      console.error('❌ Error starting transcription:', error);
      throw error;
    }
  }

  // Poll for job status
  async pollJobStatus(jobId, maxAttempts = 60, intervalMs = 2000) {
    let attempts = 0;
    
    while (attempts < maxAttempts) {
      try {
        const response = await fetch(`${this.baseUrl}/api/v1/transcription/status/${jobId}`, {
          headers: this.headers
        });

        if (response.ok) {
          const data = await response.json();
          const status = data.data.status;
          
          console.log(`📊 Job ${jobId} status: ${status}`);
          
          if (status === 'completed') {
            console.log('✅ Transcription completed:', data.data.result);
            return data.data.result;
          } else if (status === 'failed') {
            throw new Error(`Transcription failed: ${data.data.error}`);
          } else if (status === 'processing') {
            console.log('⏳ Still processing...');
          }
        } else {
          throw new Error(`Status check failed: ${response.status}`);
        }
      } catch (error) {
        console.error('❌ Error checking status:', error);
        throw error;
      }

      // Wait before next poll
      await new Promise(resolve => setTimeout(resolve, intervalMs));
      attempts++;
    }

    throw new Error('Transcription timed out');
  }

  // Complete transcription process
  async transcribeWithPolling(audioFile, assessmentId) {
    try {
      console.log('🚀 Starting transcription...');
      
      // Start the job
      const jobId = await this.startTranscription(audioFile, assessmentId);
      
      // Poll for completion
      const result = await this.pollJobStatus(jobId);
      
      console.log('🎉 Transcription completed successfully!');
      return result;
      
    } catch (error) {
      console.error('❌ Transcription failed:', error);
      throw error;
    }
  }
}

// Usage example:
/*
const client = new AsyncTranscriptionClient(
  'https://api.testing.labendoc.com',
  'lSaWtIgjLeWUWBA%FinQI0RgVFiZJtLE'
);

// Example usage in a web app
async function handleAudioUpload(audioFile, assessmentId) {
  try {
    // Show loading state
    showLoading('Starting transcription...');
    
    // Start transcription
    const result = await client.transcribeWithPolling(audioFile, assessmentId);
    
    // Show success
    showSuccess('Transcription completed!');
    displayTranscript(result.transcript);
    
  } catch (error) {
    // Show error
    showError('Transcription failed: ' + error.message);
  }
}

// Frontend polling example
async function pollTranscriptionStatus(jobId) {
  const maxAttempts = 60; // 2 minutes max
  const intervalMs = 2000; // Check every 2 seconds
  
  for (let i = 0; i < maxAttempts; i++) {
    try {
      const response = await fetch(`/api/v1/transcription/status/${jobId}`, {
        headers: {
          'Authorization': `Bearer ${authToken}`
        }
      });
      
      const data = await response.json();
      
      if (data.data.status === 'completed') {
        return data.data.result;
      } else if (data.data.status === 'failed') {
        throw new Error(data.data.error);
      }
      
      // Update UI with progress
      updateProgress(data.data.status);
      
      // Wait before next poll
      await new Promise(resolve => setTimeout(resolve, intervalMs));
      
    } catch (error) {
      console.error('Polling error:', error);
      throw error;
    }
  }
  
  throw new Error('Transcription timed out');
}
*/

export default AsyncTranscriptionClient; 