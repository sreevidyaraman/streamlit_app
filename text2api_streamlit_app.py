{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "6bcabd54-c27d-4a6d-bd57-54e7dfdddb45",
   "metadata": {},
   "outputs": [],
   "source": [
    "import streamlit as st\n",
    "import pandas as pd"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "27ce7c65-536c-4b13-b643-5f3fb2f466d7",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2024-10-01 09:40:06.465 WARNING streamlit.runtime.state.session_state_proxy: Session state does not function when running a script without `streamlit run`\n",
      "2024-10-01 09:40:06.700 \n",
      "  \u001b[33m\u001b[1mWarning:\u001b[0m to view this Streamlit app on a browser, run it with the following\n",
      "  command:\n",
      "\n",
      "    streamlit run C:\\Users\\SreevidyaRaman\\anaconda3\\Lib\\site-packages\\ipykernel_launcher.py [ARGUMENTS]\n"
     ]
    }
   ],
   "source": [
    "number = st.slider(\"Pick a number\", 0, 100)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "id": "35a38438-e93c-430a-86bd-d3ffc0dd6ed9",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "Traceback (most recent call last):\n",
      "  File \"C:\\Users\\SreevidyaRaman\\anaconda3\\Scripts\\streamlit-script.py\", line 6, in <module>\n",
      "    from streamlit.cli import main\n",
      "ModuleNotFoundError: No module named 'streamlit.cli'\n"
     ]
    }
   ],
   "source": [
    "streamlit run C:\\Users\\SreevidyaRaman\\anaconda3\\Lib\\site-packages\\ipykernel_launcher.py"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "4395a9ca-3116-47c7-b687-7a2bd18310f7",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
