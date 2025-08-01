import streamlit as st
from retell import Retell, APIStatusError
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="AI Voice Agent", 
    layout="wide",
    page_icon="🎙️",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 3rem;
        font-weight: 300;
    }
    
    .agent-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        margin: 1rem;
        border: 1px solid #e9ecef;
        transition: all 0.3s ease;
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .agent-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    }
    
    .agent-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    .dental-card::before {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
    }
    
    .restaurant-card::before {
        background: linear-gradient(90deg, #fa709a 0%, #fee140 100%);
    }
    
    .agent-icon {
        font-size: 4rem;
        text-align: center;
        margin-bottom: 1rem;
        display: block;
    }
    
    .agent-title {
        font-size: 1.8rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
        color: #2c3e50;
    }
    
    .agent-description {
        text-align: center;
        color: #6c757d;
        margin-bottom: 2rem;
        line-height: 1.6;
        font-size: 1rem;
    }
    
    .agent-features {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 2rem;
    }
    
    .agent-features ul {
        margin: 0;
        padding-left: 1.2rem;
        color: #495057;
    }
    
    .agent-features li {
        margin-bottom: 0.5rem;
    }
    
    .status-success {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 2rem 0;
        box-shadow: 0 5px 15px rgba(21, 87, 36, 0.1);
    }
    
    .status-error {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 2rem 0;
        box-shadow: 0 5px 15px rgba(114, 28, 36, 0.1);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 1rem 2rem;
        font-weight: bold;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    .dental-button > button {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        box-shadow: 0 5px 15px rgba(79, 172, 254, 0.3);
    }
    
    .dental-button > button:hover {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        box-shadow: 0 8px 25px rgba(79, 172, 254, 0.4);
    }
    
    .restaurant-button > button {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        box-shadow: 0 5px 15px rgba(250, 112, 154, 0.3);
    }
    
    .restaurant-button > button:hover {
        background: linear-gradient(135deg, #fee140 0%, #fa709a 100%);
        box-shadow: 0 8px 25px rgba(250, 112, 154, 0.4);
    }
    
    .metrics-container {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
        margin: 1rem 0;
    }
    
    .voice-interface {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        margin: 2rem 0;
    }
    
    .instructions-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #2196f3;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Retell
retell = Retell(api_key="key_1b0492306abc8fc752453c8aba22")

AGENTS = {
    "dental": "agent_4deac7a40e9e59967e58066b88",
    "restaurant": "agent_9dc9c953b22b75512d0d63c748",
}

# Agent information
AGENT_INFO = {
    "dental": {
        "icon": "🦷",
        "title": "Dental Assistant",
        "description": "Your AI-powered dental care companion, ready to help with appointments, procedures, and oral health guidance.",
        "features": [
            "Schedule dental appointments",
            "Answer oral health questions",
            "Provide procedure information",
            "Offer dental care tips",
            "Emergency dental guidance"
        ]
    },
    "restaurant": {
        "icon": "🍽️",
        "title": "Restaurant Assistant",
        "description": "Your personal dining concierge, here to assist with reservations, menu recommendations, and dining experiences.",
        "features": [
            "Make restaurant reservations",
            "Provide menu recommendations",
            "Answer dietary questions",
            "Special occasion planning",
            "Local dining suggestions"
        ]
    }
}

# Header
st.markdown('<h1 class="main-header">🎙️  AI Voice Agents</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Experience the future of AI conversation • Choose your specialized assistant below</p>', unsafe_allow_html=True)

# Initialize session state for selected agent
if 'selected_agent' not in st.session_state:
    st.session_state.selected_agent = None
if 'call_active' not in st.session_state:
    st.session_state.call_active = False

# Agent selection cards
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown(f"""
    <div class="agent-card dental-card">
        <div class="agent-icon">{AGENT_INFO['dental']['icon']}</div>
        <div class="agent-title">{AGENT_INFO['dental']['title']}</div>
        <div class="agent-description">{AGENT_INFO['dental']['description']}</div>
        <div class="agent-features">
            <strong>🌟 Key Features:</strong>
            <ul>
                {''.join([f'<li>{feature}</li>' for feature in AGENT_INFO['dental']['features']])}
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    dental_button = st.button("🎙️ Start Dental Consultation", key="dental_btn", help="Begin conversation with dental assistant")
    st.markdown('<style>.dental-button { }</style>', unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="agent-card restaurant-card">
        <div class="agent-icon">{AGENT_INFO['restaurant']['icon']}</div>
        <div class="agent-title">{AGENT_INFO['restaurant']['title']}</div>
        <div class="agent-description">{AGENT_INFO['restaurant']['description']}</div>
        <div class="agent-features">
            <strong>🌟 Key Features:</strong>
            <ul>
                {''.join([f'<li>{feature}</li>' for feature in AGENT_INFO['restaurant']['features']])}
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    restaurant_button = st.button("🎙️ Start Restaurant Assistance", key="restaurant_btn", help="Begin conversation with restaurant assistant")

# Handle button clicks
if dental_button:
    st.session_state.selected_agent = "dental"
    st.session_state.call_active = True

if restaurant_button:
    st.session_state.selected_agent = "restaurant"
    st.session_state.call_active = True

# Handle conversation start
if st.session_state.call_active and st.session_state.selected_agent:
    agent = st.session_state.selected_agent
    agent_info = AGENT_INFO[agent]
    
    st.markdown("---")
    st.markdown(f"## 🚀 Initializing {agent_info['title']}")
    
    with st.spinner(f"🔄 Setting up your {agent.title()} AI assistant..."):
        try:
            agent_id = AGENTS[agent]
            response = retell.call.create_web_call(agent_id=agent_id)
            data = response.to_dict()
            
            # Success message
            st.markdown(f"""
            <div class="status-success">
                <h3>✅ {agent_info['title']} Ready!</h3>
                <p>Your AI {agent} assistant is now active and ready to help you. The voice interface will load below.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Call information in a beautiful container
            st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
            st.markdown("### 📊 Session Information")
            
            col_info1, col_info2, col_info3, col_info4 = st.columns(4)
            
            with col_info1:
                st.metric("🤖 Agent Type", agent_info['title'])
            with col_info2:
                st.metric("📞 Call ID", data.get("call_id", "N/A")[:8] + "...")
            with col_info3:
                st.metric("🟢 Status", "Active")
            with col_info4:
                st.metric("🎵 Quality", "24kHz HD")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Expandable section for technical details
            with st.expander("🔧 Technical Details", expanded=False):
                st.json(data)
            
            access_token = data.get("access_token")
            
            if access_token:
                st.markdown('<div class="voice-interface">', unsafe_allow_html=True)
                st.markdown("### 🎧 Voice Interface")
                
                st.markdown(f"""
                <div class="instructions-box">
                    <h4>📢 How to interact with your {agent_info['title']}:</h4>
                    <ul>
                        <li><strong>🎤 Allow microphone access</strong> when your browser prompts you</li>
                        <li><strong>🗣️ Speak naturally</strong> - no need to use special commands</li>
                        <li><strong>👂 Listen carefully</strong> - the AI will respond with voice</li>
                        <li><strong>📝 Watch the transcript</strong> below for real-time conversation tracking</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
                # Enhanced JavaScript integration
                components.html(f"""
                <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 25px; background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
                    <div id="status" style="padding: 15px; margin-bottom: 20px; background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); border-radius: 15px; border-left: 5px solid #f39c12; box-shadow: 0 5px 15px rgba(243,156,18,0.2);">
                        <strong style="font-size: 1.1rem;">🔄 Initializing {agent_info['title']} voice client...</strong>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: 1fr 200px; gap: 20px; margin-bottom: 20px;">
                        <div id="transcript-container" style="background: white; padding: 20px; border-radius: 15px; min-height: 300px; border: 1px solid #dee2e6; box-shadow: 0 5px 15px rgba(0,0,0,0.05);">
                            <h4 style="margin-top: 0; color: #495057; display: flex; align-items: center; gap: 10px;">
                                <span style="font-size: 1.5rem;">📝</span> Live Conversation
                            </h4>
                            <div id="transcript" style="font-family: 'Courier New', monospace; color: #6c757d; line-height: 1.6;">
                                <div style="text-align: center; padding: 40px; color: #adb5bd;">
                                    <div style="font-size: 3rem; margin-bottom: 10px;">{agent_info['icon']}</div>
                                    <p>Waiting for conversation to begin...</p>
                                </div>
                            </div>
                        </div>
                        
                        <div style="display: flex; flex-direction: column; gap: 15px;">
                            <div id="voice-status" style="background: white; padding: 15px; border-radius: 15px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.05);">
                                <div style="font-size: 2rem; margin-bottom: 10px;">🎤</div>
                                <div style="font-size: 0.9rem; color: #6c757d;">Voice Status</div>
                                <div id="voice-indicator" style="font-weight: bold; color: #28a745;">Initializing</div>
                            </div>
                            
                            <div style="background: white; padding: 15px; border-radius: 15px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.05);">
                                <div style="font-size: 2rem; margin-bottom: 10px;">⏱️</div>
                                <div style="font-size: 0.9rem; color: #6c757d;">Session Time</div>
                                <div id="session-timer" style="font-weight: bold; color: #007bff;">00:00</div>
                            </div>
                            
                            <div style="background: white; padding: 15px; border-radius: 15px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.05);">
                                <div style="font-size: 2rem; margin-bottom: 10px;">💬</div>
                                <div style="font-size: 0.9rem; color: #6c757d;">Messages</div>
                                <div id="message-count" style="font-weight: bold; color: #6f42c1;">0</div>
                            </div>
                        </div>
                    </div>
                </div>

                <script type="module">
                    import {{ RetellWebClient }} from 'https://cdn.jsdelivr.net/npm/retell-client-js-sdk/+esm';
                    
                    const statusDiv = document.getElementById('status');
                    const transcriptDiv = document.getElementById('transcript');
                    const voiceIndicator = document.getElementById('voice-indicator');
                    const sessionTimer = document.getElementById('session-timer');
                    const messageCount = document.getElementById('message-count');
                    
                    let startTime = Date.now();
                    let messageCounter = 0;
                    
                    // Update session timer
                    setInterval(() => {{
                        const elapsed = Math.floor((Date.now() - startTime) / 1000);
                        const minutes = Math.floor(elapsed / 60);
                        const seconds = elapsed % 60;
                        sessionTimer.textContent = `${{minutes.toString().padStart(2, '0')}}:${{seconds.toString().padStart(2, '0')}}`;
                    }}, 1000);
                    
                    function updateStatus(message, type = 'info') {{
                        const styles = {{
                            'success': 'background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); border-left-color: #28a745;',
                            'error': 'background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%); border-left-color: #dc3545;',
                            'info': 'background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%); border-left-color: #17a2b8;',
                            'warning': 'background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); border-left-color: #f39c12;'
                        }};
                        statusDiv.style.cssText = styles[type] + 'padding: 15px; margin-bottom: 20px; border-radius: 15px; border-left: 5px solid; box-shadow: 0 5px 15px rgba(0,0,0,0.1);';
                        statusDiv.innerHTML = `<strong style="font-size: 1.1rem;">${{message}}</strong>`;
                    }}
                    
                    function addTranscript(text, speaker = 'user') {{
                        const timestamp = new Date().toLocaleTimeString();
                        const speakerIcon = speaker === 'agent' ? '{agent_info['icon']}' : '👤';
                        const speakerColor = speaker === 'agent' ? '#007bff' : '#28a745';
                        const bgColor = speaker === 'agent' ? '#f8f9ff' : '#f0fff4';
                        
                        if (transcriptDiv.innerHTML.includes('Waiting for conversation')) {{
                            transcriptDiv.innerHTML = '';
                        }}
                        
                        transcriptDiv.innerHTML += `
                            <div style="margin: 12px 0; padding: 15px; border-left: 4px solid ${{speakerColor}}; background: ${{bgColor}}; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                    <strong style="color: ${{speakerColor}}; display: flex; align-items: center; gap: 8px;">
                                        <span style="font-size: 1.2rem;">${{speakerIcon}}</span>
                                        ${{speaker.charAt(0).toUpperCase() + speaker.slice(1)}}
                                    </strong>
                                    <small style="color: #6c757d; font-size: 0.8rem;">${{timestamp}}</small>
                                </div>
                                <div style="color: #495057; line-height: 1.5;">${{text}}</div>
                            </div>
                        `;
                        transcriptDiv.scrollTop = transcriptDiv.scrollHeight;
                        
                        messageCounter++;
                        messageCount.textContent = messageCounter;
                    }}
                    
                    try {{
                        const client = new RetellWebClient();
                        
                        updateStatus('🎙️ Connecting to {agent_info['title']}...', 'info');
                        voiceIndicator.textContent = 'Connecting';
                        voiceIndicator.style.color = '#ffc107';
                        
                        await client.startCall({{
                            accessToken: "{access_token}",
                            sampleRate: 24000
                        }});
                        
                        updateStatus('✅ {agent_info['title']} is ready! Start speaking now...', 'success');
                        voiceIndicator.textContent = 'Ready';
                        voiceIndicator.style.color = '#28a745';
                        
                        transcriptDiv.innerHTML = `
                            <div style="text-align: center; padding: 30px; background: linear-gradient(135deg, #e8f5e8 0%, #d4edda 100%); border-radius: 15px; margin-bottom: 15px;">
                                <div style="font-size: 3rem; margin-bottom: 15px;">{agent_info['icon']}</div>
                                <h3 style="color: #28a745; margin-bottom: 10px;">🎉 {agent_info['title']} Active!</h3>
                                <p style="color: #155724; margin: 0;">Your conversation will appear here in real-time</p>
                            </div>
                        `;
                        
                        client.on('update', (update) => {{
                            if (update.transcript) {{
                                addTranscript(update.transcript, 'user');
                            }}
                        }});
                        
                        client.on('agent_start_talking', () => {{
                            updateStatus('🤖 {agent_info['title']} is speaking...', 'info');
                            voiceIndicator.textContent = 'AI Speaking';
                            voiceIndicator.style.color = '#007bff';
                        }});
                        
                        client.on('agent_stop_talking', () => {{
                            updateStatus('👂 Listening for your response...', 'success');
                            voiceIndicator.textContent = 'Listening';
                            voiceIndicator.style.color = '#28a745';
                        }});
                        
                        client.on('call_ended', () => {{
                            updateStatus('📞 Conversation ended - Thank you!', 'warning');
                            voiceIndicator.textContent = 'Ended';
                            voiceIndicator.style.color = '#6c757d';
                        }});
                        
                    }} catch (err) {{
                        updateStatus(`❌ Connection failed: ${{err.message}}`, 'error');
                        voiceIndicator.textContent = 'Error';
                        voiceIndicator.style.color = '#dc3545';
                        console.error('Call error:', err);
                    }}
                </script>
                """, height=700)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Reset button
                if st.button("🔄 Start New Conversation", help="Reset and choose a different agent"):
                    st.session_state.selected_agent = None
                    st.session_state.call_active = False
                    st.rerun()
                    
            else:
                st.markdown("""
                <div class="status-error">
                    <h4>❌ Access Token Missing</h4>
                    <p>No access token received from the API. Cannot initiate the voice call.</p>
                </div>
                """, unsafe_allow_html=True)
                
        except APIStatusError as e:
            st.markdown(f"""
            <div class="status-error">
                <h4>🚫 Retell API Error</h4>
                <p><strong>Status Code:</strong> {e.status_code}</p>
                <p><strong>Error Details:</strong> {e.get_body_text()}</p>
                <p><em>Please try again or contact support if the issue persists.</em></p>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.markdown(f"""
            <div class="status-error">
                <h4>⚠️ Unexpected Error</h4>
                <p><strong>Error:</strong> {str(e)}</p>
                <p><em>Please refresh the page and try again.</em></p>
            </div>
            """, unsafe_allow_html=True)

# Footer
if not st.session_state.call_active:
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 3rem; padding: 2rem; background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 20px;">
        <h4 style="color: #495057; margin-bottom: 1rem;">🔒 Privacy & Security</h4>
        <p style="margin-bottom: 1rem;">Your conversations are secure, encrypted, and never stored permanently</p>
        <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap; margin-top: 1.5rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.2rem;">🛡️</span>
                <span>End-to-End Encrypted</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.2rem;">🚀</span>
                <span>Powered by  AI</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.2rem;">⚡</span>
                <span>Built with Streamlit</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
